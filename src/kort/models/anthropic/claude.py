import time
from typing import Optional

from anthropic import Anthropic
from anthropic.types.thinking_config_disabled_param import ThinkingConfigDisabledParam
from anthropic.types.thinking_config_enabled_param import ThinkingConfigEnabledParam

from ..base_model import BaseModel


class ClaudeModel(BaseModel):
    model_org: str = "anthropic"
    _need_api_key: bool = True

    def __init__(
        self,
        model_name: str,
        api_key: Optional[str] = None,
        evaluation: bool = False,
        *args,
        **kwargs,
    ):
        self.model_name = model_name
        super().__init__(api_key=api_key, evaluation=evaluation, *args, **kwargs)
        self.client = Anthropic(api_key=api_key)

    def inference(self, input: str) -> str:
        try:
            result = self.client.messages.create(
                model=self.model_name,  # type: ignore[arg-type]
                messages=[{"role": "user", "content": input}],
                max_tokens=8192 if not self.evaluation else 16512,
                thinking=ThinkingConfigDisabledParam(type="disabled")
                if not self.evaluation
                else ThinkingConfigEnabledParam(type="enabled", budget_tokens=16000),
            )
            if result.content[-1].type != "text":
                raise ValueError(f"Unexpected content type: {result.content[-1].type}")
            output = result.content[-1].text
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
