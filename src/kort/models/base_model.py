import time
from typing import Optional


class BaseModel:
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
        api_key: Optional[str] = None,
        evaluation: bool = False,
        device: Optional[str] = None,
        stop: Optional[str] = None,
    ):
        """
        Initialize the base model with the specified model name and API key.

        Args:
            model_name (str): The name of model to initialize.
            api_key (str, optional): The API key for accessing the model. Defaults to None.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if self.model_org == "BaseModel":
            raise ValueError("BaseModel cannot be instantiated directly.")

        if self._need_api_key and api_key is None:
            raise ValueError("API key is required for this model.")
        if api_key is not None:
            self.api_key = api_key

        self.evaluation = evaluation
        self.device = device
        self.stop = stop

    def inference(self, input: str) -> str:
        """
        Perform inference on the input data.

        Args:
            input (str): The input data for inference.

        Returns:
            str: The result of the inference.
        """
        raise NotImplementedError("Inference method not implemented.")

    def error_retry(self) -> bool:
        self.error = self.error if self.error else 0
        if time.time() - self.last_error > 6:
            self.error = 0
        self.last_error = time.time()
        self.error += 1
        if self.error > 5:
            print(f"Error: {self.error} times, stopping...")
            self.error = 0
            return False
        return True
