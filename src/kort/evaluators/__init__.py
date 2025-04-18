from .base_evaluator import BaseEvaluator
from .from_batch import BatchModelEvaluator
from .from_model import ModelEvaluator
from .human import HumanEvaluator

__all__ = [
    "BaseEvaluator",
    "BatchModelEvaluator",
    "ModelEvaluator",
    "HumanEvaluator",
]


def get_evaluator(evaluator_name: str) -> BaseEvaluator:
    """
    Get the evaluator class based on the evaluator name.

    Args:
        evaluator_name (str): The name of the evaluator to retrieve.

    Returns:
        BaseEvaluator: The corresponding evaluator class.
    """
    evaluator_class_name = evaluator_name + "Evaluator"
    lower_globals = {k.lower(): v for k, v in globals().items()}
    evaluator_class = lower_globals.get(evaluator_class_name.lower())
    if evaluator_class is None:
        raise ValueError(f"Evaluator '{evaluator_name}' not found.")
    return evaluator_class


def get_evaluator_list() -> list[str]:
    """
    Get a list of available evaluator names.

    Returns:
        list[str]: A list of available evaluator names.
    """
    return [
        k.lower()[:-9]
        for k in globals().keys()
        if k.endswith("Evaluator")
        and k not in ["BaseEvaluator", "ModelEvaluator", "BatchModelEvaluator"]
    ]
