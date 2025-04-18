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
    leaderboard_data = []

    def __init__(self, input_dir: str):
        self.input_dir = input_dir
        self.load_data()

    def get_summary(self, evaluated: Evaluated):
        """
        Get a summary of the evaluated model.
        """
        sum_overall_score: int = 0
        sum_category_scores: dict[Categories, int] = {}
        count_category: dict[Categories, int] = {}
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

    def load_data(self):
        json_files = [f for f in os.listdir(self.input_dir) if f.endswith(".json")]

        for file in json_files:
            file_path = os.path.join(self.input_dir, file)
            with open(file_path, "r") as f:
                data = json.load(f)
            try:
                evaluated = Evaluated(**data)
                self.data.append(self.get_summary(evaluated))
            except Exception:
                continue

        common_categories = self.data[0].category_scores.keys()
        for model in self.data:
            self.leaderboard_data.append(
                {
                    "Model Name": model.model_name,
                    "Overall Score": round(model.overall_score),
                    **{
                        category.name: round(model.category_scores[category])
                        for category in common_categories
                    },
                }
            )

    def launch(self):
        """
        Launch the leaderboard.
        """
        raise NotImplementedError("Subclasses should implement this method.")
