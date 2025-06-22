import time
from abc import ABC, abstractmethod
from typing import Optional

from ..config import eval_config
from ..utils.exceptions import APIKeyError, ModelNotFoundError
from ..utils.retry import retry_with_backoff


class BaseModel(ABC):
    """
    Base class for all models in the application.
    """

    model_org: str = "BaseModel"
    model_name: str = "BaseModel"
    _need_api_key: bool = False
    error = 0
    last_error = time.time()

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        evaluation: bool = False,
        device: Optional[str] = None,
        stop: Optional[str] = None,
    ):
        """
        Initialize the base model with the specified model name and API key.

        Args:
            api_key: The API key for accessing the model. Defaults to None.
            evaluation: Whether this model is being used for evaluation.
            device: The device to use for the model.
            stop: Stop sequence for the model.

        Raises:
            APIKeyError: If API key is required but not provided.
            ModelNotFoundError: If the model cannot be instantiated.
        """
        if self.model_org == "BaseModel":
            raise ModelNotFoundError("BaseModel cannot be instantiated directly.")

        if self._need_api_key and api_key is None:
            raise APIKeyError("API key is required for this model.")

        if api_key is not None:
            self.api_key = api_key

        self.evaluation = evaluation
        self.device = device
        self.stop = stop

    @abstractmethod
    def inference(self, input: str) -> str:
        """
        Perform inference on the input data.

        Args:
            input: The input data for inference.

        Returns:
            The result of the inference.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Inference method not implemented.")

    def error_retry(self) -> bool:
        """
        Handle error retry logic with improved backoff.

        Returns:
            True if should retry, False if should stop.
        """
        self.error = self.error if self.error else 0
        if time.time() - self.last_error > eval_config.retry_delay * 6:
            self.error = 0
        self.last_error = time.time()
        self.error += 1

        if self.error > eval_config.max_retries:
            print(f"Error: {self.error} times, stopping...")
            self.error = 0
            return False
        return True

    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def safe_inference(self, input: str) -> str:
        """
        Perform inference with automatic retry on failure.

        Args:
            input: The input data for inference.

        Returns:
            The result of the inference.
        """
        return self.inference(input)
