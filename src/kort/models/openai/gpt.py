import time
from typing import Optional

from openai import OpenAI

from ..base_model import BaseModel


class OpenAIModel(BaseModel):
    model_org: str = "openai"
    _need_api_key: bool = True

    def __init__(self, model_name: str, api_key: Optional[str] = None, *args, **kwargs):
        self.model_name = model_name
        super().__init__(api_key=api_key, *args, **kwargs)
        self.client = OpenAI(api_key=self.api_key)

    def inference(self, input: str) -> str:
        try:
            output = self.client.responses.create(
                model=self.model_name, input=input
            ).output_text
        except Exception as e:
            print(e)
            if self.error_retry():
                print("Server error, retrying 1 second later...")
                time.sleep(1)
                output = self.inference(input)
            else:
                raise ValueError(f"Server error occurred for {self.model_name}.")

        if output == "" or output is None:
            if self.error_retry():
                print("Error occurred, retrying...")
                return self.inference(input)
            else:
                raise ValueError(f"Translation failed for {self.model_name}.")

        return output
