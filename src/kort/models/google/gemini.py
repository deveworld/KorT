import time
from typing import Optional

from google import genai
from google.genai import errors, types

from ..base_model import BaseModel


class GeminiModel(BaseModel):
    model_org: str = "google"
    _need_api_key: bool = True

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        temperature: float = 0.3,
        max_output_tokens: Optional[int] = None,
        evaluation: bool = False,
        *args,
        **kwargs,
    ):
        self.model_name = model_name
        super().__init__(api_key=api_key, *args, **kwargs)
        self.client = genai.Client(api_key=self.api_key)
        self.temperature = temperature
        self.max_output_tokens = (
            max_output_tokens if max_output_tokens else 16512 if evaluation else 8192
        )
        self.evaluation = evaluation

    def get_config(self):
        return types.GenerateContentConfig(
            max_output_tokens=self.max_output_tokens,
            temperature=self.temperature,
            safety_settings=[
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
                types.SafetySetting(
                    category=types.HarmCategory.HARM_CATEGORY_CIVIC_INTEGRITY,
                    threshold=types.HarmBlockThreshold.BLOCK_NONE,
                ),
            ],
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_budget=16000,
            )
            if self.evaluation
            else None,
        )

    def inference(self, input: str) -> str:
        try:
            output = self.client.models.generate_content(
                model=self.model_name,
                config=self.get_config(),
                contents=input,
            ).text
        except errors.ClientError as e:
            print(e)
            if self.error_retry():
                print("Server error, retrying 5 second later...")
                time.sleep(5)
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
