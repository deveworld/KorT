from ..transformer_model import TransformersModel


class GemagoModel(TransformersModel):
    """
    Model class for the Gemago model.
    """

    _need_api_key = False

    def __init__(self, model_name: str, evaluation: bool = False, *args, **kwargs):
        if evaluation:
            raise ValueError("Gugugo model does not support evaluation mode.")
        if "gemago" not in model_name.lower():
            raise ValueError("Gemago model name must include 'gemago'")
        super().__init__(model_name, evaluation=False, *args, **kwargs)

    def inference(self, input: str) -> str:
        input_ids = self.tokenizer(input, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **input_ids,
            max_length=128,
            temperature=0.3,
            top_p=0.8,
            do_sample=True,
        )
        output = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[
            0
        ].replace(input, "")
        return output
