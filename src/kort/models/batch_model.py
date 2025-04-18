from ..data import BatchStatus
from .base_model import BaseModel


class BatchModel(BaseModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def batch_inference(self, inputs: dict[str, str]) -> str:
        """
        Perform batch inference on a list of inputs.

        Args:
            inputs (list): A list of input strings to be processed.

        Returns:
            str: The id of the batch job.
        """
        raise NotImplementedError("Batch inference is not implemented for this model.")

    def batch_status(self, job_id: str) -> BatchStatus:
        """
        Check the status of a batch job.

        Args:
            job_id (str): The id of the batch job.

        Returns:
            str: The status of the batch job.
        """
        raise NotImplementedError("Batch status is not implemented for this model.")

    def batch_result(self, job_id: str) -> dict[str, str]:
        """
        Get the result of a batch job.

        Args:
            job_id (str): The id of the batch job.

        Returns:
            dict[str, str]: The result of the batch job.
        """
        raise NotImplementedError("Batch result is not implemented for this model.")
