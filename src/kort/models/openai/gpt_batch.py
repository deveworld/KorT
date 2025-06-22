import json
import os
from typing import Optional

from openai import OpenAI

from ...data import BatchStatus
from ..batch_model import BatchModel


class OpenAIBatchModel(BatchModel):
    model_org: str = "openai"
    _need_api_key: bool = True

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        evaluation: bool = False,
        *args,
        **kwargs,
    ):
        super().__init__(model_name, api_key, evaluation=evaluation, *args, **kwargs)
        self.client = OpenAI(api_key=self.api_key)

    def batch_inference(self, inputs: dict[str, str]) -> str:
        data: list[dict] = []
        for key, value in inputs.items():
            data.append(
                {
                    "custom_id": key,
                    "method": "POST",
                    "url": "/v1/chat/completions",
                    "body": {
                        "model": self.model_name,
                        "messages": [{"role": "user", "content": value}],
                        "max_completion_tokens": 16512 if self.evaluation else 8192,
                    },
                }
            )

        with open("temp.jsonl", "w") as f:
            f.write("\n".join([json.dumps(d) for d in data]))

        batch_input_file = self.client.files.create(
            file=open("temp.jsonl", "rb"), purpose="batch"
        )
        batch_input_file_id = batch_input_file.id

        job = self.client.batches.create(
            input_file_id=batch_input_file_id,
            endpoint="/v1/chat/completions",
            completion_window="24h",
        )

        os.remove("temp.jsonl")

        return job.id

    def batch_status(self, job_id: str) -> BatchStatus:
        job = self.client.batches.retrieve(job_id)
        if job.status in ["validating", "in_progress", "finalizing"]:
            return BatchStatus.IN_PROGRESS
        elif job.status == "completed":
            return BatchStatus.COMPLETED
        elif job.status in ["failed", "expired", "cancelling", "cancelled"]:
            return BatchStatus.FAILED
        else:
            return BatchStatus.UNKNOWN

    def batch_result(self, job_id: str) -> dict[str, str]:
        if not self.batch_status(job_id) == BatchStatus.COMPLETED:
            raise Exception(f"Job {job_id} is not completed yet.")

        job = self.client.batches.retrieve(job_id)
        if not job.output_file_id:
            raise Exception(f"Job {job_id} has no output file.")
        jsonl = self.client.files.content(job.output_file_id).text

        results = {}
        for data in jsonl.splitlines():
            loaded_data = json.loads(data)
            results[loaded_data["custom_id"]] = loaded_data["response"]["body"][
                "choices"
            ][-1]["message"]["content"]

        return results
