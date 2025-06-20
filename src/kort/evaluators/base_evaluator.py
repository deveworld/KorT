from typing import Optional

from ..data import EvaluationResult, GenerationExample


class BaseEvaluator:
    """
    Base class for all evaluators.
    """

    evaluator_org: str = "BaseEvaluator"
    evaluator_name: str = "BaseEvaluator"
    _need_api_key: bool = False
    error = 0

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the base evaluator with the specified evaluator name and API key.

        Args:
            evaluator_name (str): The name of the evaluator to initialize.
            api_key (str, optional): The API key for accessing the evaluator. Defaults to None.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if self.evaluator_org == "BaseEvaluator":
            raise ValueError("BaseEvaluator cannot be instantiated directly.")

        if self._need_api_key and api_key is None:
            raise ValueError("API key is required for this evaluator.")
        if api_key is not None:
            self.api_key = api_key

    def evaluate(self, generated: GenerationExample) -> EvaluationResult:
        """
        Evaluate the generated example.

        Args:
            generated (GenerationExample): The generated example to evaluate.

        Returns:
            EvaluationResult: The evaluation result.
        """
        raise NotImplementedError("Evaluate method not implemented.")

    def error_retry(self) -> bool:
        self.error = self.error if self.error else 0
        self.error += 1
        if self.error > 5:
            print(f"Error: {self.error} times, stopping...")
            self.error = 0
            return False
        return True
