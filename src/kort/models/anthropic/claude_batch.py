from anthropic import Anthropic
from anthropic.types.content_block import ContentBlock
from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
from anthropic.types.messages.batch_create_params import Request
from anthropic.types.messages.message_batch_individual_response import (
    MessageBatchIndividualResponse,
)

from ...data import BatchStatus
from ..batch_model import BatchModel


class ClaudeBatchModel(BatchModel):
    model_org: str = "anthropic"
    _need_api_key: bool = True

    def __init__(
        self,
        model_name: str,
        api_key: str = None,
        evaluation: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(model_name, api_key, evaluation=evaluation, *args, **kwargs)
        self.client = Anthropic(api_key=api_key)

    def batch_inference(self, inputs: dict[str, str]) -> str:
        data: list[Request] = []
        for key, value in inputs.items():
            data.append(
                Request(
                    custom_id=key,
                    params=MessageCreateParamsNonStreaming(
                        model=self.model_name,
                        max_tokens=8192 if not self.evaluation else 16512,
                        thinking={"type": "disabled"}
                        if not self.evaluation
                        else {"type": "enabled", "budget_tokens": 16000},
                        messages=[{"role": "user", "content": value}],
                    ),
                )
            )
        job = self.client.messages.batches.create(requests=data)
        return job.id

    def batch_status(self, job_id: str) -> BatchStatus:
        job = self.client.messages.batches.retrieve(job_id)
        if job.processing_status == "in_progress":
            return BatchStatus.IN_PROGRESS
        elif job.processing_status == "ended":
            return BatchStatus.COMPLETED
        elif job.processing_status == "canceling":
            return BatchStatus.FAILED
        else:
            return BatchStatus.UNKNOWN

    def batch_result(self, job_id: str) -> dict[str, str]:
        if not self.batch_status(job_id) == BatchStatus.COMPLETED:
            raise Exception(f"Job {job_id} is not completed yet.")

        job_results: list[MessageBatchIndividualResponse] = (
            self.client.messages.batches.results(job_id)
        )
        results = {}
        for batch in job_results:
            output: ContentBlock = batch.result.message.content[-1]
            results[batch.custom_id] = output.text

        return results
