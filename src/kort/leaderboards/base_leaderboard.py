import json
import os

from pydantic import BaseModel

from ..data import Categories, Evaluated, EvaluationMetadata


class ModelSummary(BaseModel):
    """
    A summary of the model.
    """

    model_name: str
    overall_score: float
    category_scores: dict[Categories, float]


class BaseLeaderBoard:
    """
    Base class for leaderboards.
    """

    data: list[ModelSummary] = []
    leaderboard_data: list[dict[str, str | float]] = []
    raw_data: list[dict] = []

    def __init__(self, input_dir: str) -> None:
        self.input_dir = input_dir
        self.load_data()

    def get_summary(self, evaluated: Evaluated) -> ModelSummary:
        """
        Get a summary of the evaluated model.
        """
        sum_overall_score: float = 0
        sum_category_scores: dict[Categories, float] = {}
        count_category: dict[Categories, float] = {}
        for result in evaluated.evaluation_results:
            sum_overall_score += result.score
            if result.generated.category not in sum_category_scores:
                sum_category_scores[result.generated.category] = 0
                count_category[result.generated.category] = 0
            sum_category_scores[result.generated.category] += result.score
            count_category[result.generated.category] += 1

        for category in sum_category_scores:
            sum_category_scores[category] /= count_category[category]
        overall_score = sum_overall_score / len(evaluated.evaluation_results)
        metadata: EvaluationMetadata = evaluated.metadata
        return ModelSummary(
            model_name=f"{metadata.gen_model_org}/{metadata.gen_model_name}",
            overall_score=overall_score,
            category_scores=sum_category_scores,
        )

    def flatten_data(self, evaluated: Evaluated):
        return {
            "model_name": f"{evaluated.metadata.gen_model_org}/{evaluated.metadata.gen_model_name}",
            "eval_model_name": f"{evaluated.metadata.eval_model_org}/{evaluated.metadata.eval_model_name}",
            "score": evaluated.metadata.mean_score,
            **{
                f"{result.generated.category.name}_{i}": result.generated.translated
                for i, result in enumerate(evaluated.evaluation_results)
            },
        }

    def load_data(self):
        json_files = [f for f in os.listdir(self.input_dir) if f.endswith(".json")]

        for file in json_files:
            file_path = os.path.join(self.input_dir, file)
            with open(file_path, "r") as f:
                data = json.load(f)
            try:
                evaluated = Evaluated.model_validate(data)
                self.data.append(self.get_summary(evaluated))
                self.raw_data.append(self.flatten_data(evaluated))
            except Exception as e:
                print(f"Error loading file {file}: {e}")
                continue

        common_categories = self.data[0].category_scores.keys()
        for model in self.data:
            self.leaderboard_data.append(
                {
                    "Model Name": model.model_name,
                    "Overall Score": model.overall_score,
                    **{
                        category.name: model.category_scores[category]
                        for category in common_categories
                    },
                }
            )

        self.leaderboard_data.sort(key=lambda x: x["Overall Score"], reverse=True)
        # round scroes
        for model in self.leaderboard_data:
            model["Overall Score"] = round(float(model["Overall Score"]), 1)
            for category in common_categories:
                model[category.name] = round(float(model[category.name]), 1)

        self.raw_data.sort(key=lambda x: x["score"], reverse=True)
        for model in self.raw_data:
            model["score"] = round(model["score"], 1)

    def launch(self) -> None:
        """
        Launch the leaderboard.
        """
        raise NotImplementedError("Subclasses should implement this method.")
