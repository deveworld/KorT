"""Gugugo model implementation for Korean-English translation."""

import importlib
from typing import Any

from transformers.generation.stopping_criteria import (
    StoppingCriteria,
    StoppingCriteriaList,
)

from ..transformer_model import TransformersModel


def _import_torch():
    """Import torch module dynamically."""
    return importlib.import_module("torch")


class StoppingCriteriaSub(StoppingCriteria):
    """Custom stopping criteria for Gugugo model."""

    def __init__(self, stops=None, encounters=1):
        super().__init__()
        self.stops = stops if stops is not None else []

    def __call__(
        self,
        input_ids: Any,  # torch.LongTensor
        scores: Any,  # torch.FloatTensor
        **kwargs,
    ) -> Any:  # torch.BoolTensor
        torch = _import_torch()
        for stop in self.stops:
            if input_ids.shape[1] >= len(stop) and torch.all(
                (stop == input_ids[0][-len(stop) :])
            ):
                return torch.tensor([True], dtype=torch.bool, device=input_ids.device)

        return torch.tensor([False], dtype=torch.bool, device=input_ids.device)


class GugugoModel(TransformersModel):
    """
    Model class for the Gugugo model.

    This model requires torch and transformers to be installed.
    """

    _need_api_key = False

    def __init__(self, model_name: str, evaluation: bool = False, *args, **kwargs):
        if evaluation:
            raise ValueError("Gugugo model does not support evaluation mode.")
        if "gugugo" not in model_name.lower():
            raise ValueError("Gugugo model name must include 'gugugo'")
        super().__init__(model_name, evaluation=False, *args, **kwargs)

    def inference(self, input: str) -> str:
        torch = _import_torch()
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
