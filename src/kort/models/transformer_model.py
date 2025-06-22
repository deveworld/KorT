from transformers import AutoModelForCausalLM, AutoTokenizer

from .base_model import BaseModel


class TransformersModel(BaseModel):
    model_org = ""

    def __init__(self, model_name: str, *, evaluation: bool, **kwargs):
        super().__init__(evaluation=evaluation, **kwargs)
        device_map = self.device if self.device else "auto"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            torch_dtype="auto",
        )
        self.model_org = model_name.split("/")[0]
        self.model_name = model_name.split("/")[-1]

    def inference(self, input: str) -> str:
        input_ids = self.tokenizer(input, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**input_ids, max_length=8192)
        output = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[
            0
        ].replace(input, "")
        return output
