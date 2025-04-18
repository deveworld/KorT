from .base_model import BaseModel


class TransformersModel(BaseModel):
    model_org = ""

    def __init__(self, model_name: str, evaluation: bool = False, *args, **kwargs):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        super().__init__(model_name, evaluation=evaluation, *args, **kwargs)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            torch_dtype="auto",
        )

    def inference(self, input: str) -> str:
        input_ids = self.tokenizer(input, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(**input_ids, max_length=8192)
        output = self.tokenizer.decode(outputs[0])
        return output
