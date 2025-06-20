from ...data import EvaluationResult, GenerationExample
from ...evaluators import BaseEvaluator


class HumanEvaluator(BaseEvaluator):
    evaluator_org = "Human"
    evaluator_name = "HumanEvaluator"

    def __init__(self):
        super().__init__()

    def evaluate(self, generated: GenerationExample) -> EvaluationResult:
        """
        Evaluate the generated example.

        Args:
            generated (GenerationExample): The generated example to evaluate.

        Returns:
            EvaluationResult: The evaluation result.
        """
        print("===========================")
        print("Please evaluate the following translation:")
        print(f"Source: {generated.source}")
        print(f"Translated: {generated.translated}")
        print(f"Reference: {generated.reference_translation}")

        score = input("Please enter a score (0-100): ")
        while not score.isdigit() or not (0 <= int(score) <= 100):
            print("Invalid score. Please enter a number between 0 and 100.")
            score = input("Please enter a score (0-100): ")
        score = int(score)

        return EvaluationResult(generated=generated, score=score)
