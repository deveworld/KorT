import torch
from transformers.generation.stopping_criteria import (
    StoppingCriteria,
    StoppingCriteriaList,
)

from ..transformer_model import TransformersModel


class StoppingCriteriaSub(StoppingCriteria):
    def __init__(self, stops=[], encounters=1):
        super().__init__()
        self.stops = [stop for stop in stops]

    def __call__(
        self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs
    ) -> torch.BoolTensor:
        for stop in self.stops:
            if input_ids.shape[1] >= len(stop) and torch.all(
                (stop == input_ids[0][-len(stop) :])
            ):
                return torch.BoolTensor([True], device=input_ids.device)

        return torch.BoolTensor([False], device=input_ids.device)


class GugugoModel(TransformersModel):
    """
    Model class for the Gugugo model.
    """

    _need_api_key = False

    def __init__(self, model_name: str, evaluation: bool = False, *args, **kwargs):
        if evaluation:
            raise ValueError("Gugugo model does not support evaluation mode.")
        if "gugugo" not in model_name.lower():
            raise ValueError("Gugugo model name must include 'gugugo'")
        super().__init__(model_name, evaluation=False, *args, **kwargs)

    def inference(self, input: str) -> str:
        stop_words_ids = torch.tensor(
            [
                [829, 45107, 29958],
                [1533, 45107, 29958],
                [829, 45107, 29958],
                [21106, 45107, 29958],
            ]
        ).to(self.model.device)
        stopping_criteria = StoppingCriteriaList(
            [StoppingCriteriaSub(stops=stop_words_ids)]
        )

        input_ids = self.tokenizer(input, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **input_ids,
            max_length=128,
            do_sample=True,
            temperature=0.3,
            num_beams=5,
            stopping_criteria=stopping_criteria,
        )
        output = (
            self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
            .replace(input, "")
            .replace("</끝>", "")
        )
        return output
