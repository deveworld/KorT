import re
from typing import Optional

from ..data import PROMPTS, EvaluationResult, GenerationExample, PromptTask
from ..evaluators import BaseEvaluator
from ..models import BaseModel, get_model


class ModelEvaluator(BaseEvaluator):
    def __init__(self, model_type: str, model_name: str, api_key: Optional[str] = None):
        self.model_name = model_name
        self.model: BaseModel = get_model(model_type)(api_key=api_key, evaluation=True)
        if not self.model:
            raise ValueError(f"Model {model_type} not found.")
        self.evaluator_org = self.model.model_org
        self.evaluator_name = self.model.model_name
        super().__init__(self.evaluator_name)

    def evaluate(self, generated: GenerationExample) -> EvaluationResult:
        """
        Evaluate the generated example.

        Args:
            generated (GenerationExample): The generated example to evaluate.

        Returns:
            EvaluationResult: The evaluation result.
        """
        prompt = PROMPTS[PromptTask.EVALUATE].format(
            source_text=generated.source,
            translation_text=generated.translated,
            reference_translation=generated.reference_translation,
            source_lang=generated.source_lang.to_iso639_3(),
            target_lang=generated.target_lang.to_iso639_3(),
        )

        result = self.model.inference(prompt)
        if not result:
            raise ValueError(f"Evaluation failed for {self.evaluator_name}.")

        pattern = r"[-+]?\d*\.?\d+"
        numbers = re.findall(pattern, result)
        if result is None or not numbers:
            raise ValueError(f"Invalid evaluation result format: {result}")

        score = float(numbers[-1].strip().strip("\n"))
        return EvaluationResult(generated=generated, score=score)
