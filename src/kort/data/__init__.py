from enum import Enum

from .evaluate import Evaluated, EvaluationMetadata, EvaluationResult
from .generate import (
    EVAL_DATA,
    Categories,
    Example,
    Generated,
    GeneratedExample,
    GenerationMetadata,
)
from .lang_code import LangCode
from .prompts import PROMPTS, PromptTask

__all__ = [
    "LangCode",
    "Categories",
    "Example",
    "Generated",
    "GenerationMetadata",
    "EVAL_DATA",
    "GeneratedExample",
    "EvaluationResult",
    "EvaluationMetadata",
    "Evaluated",
    "PROMPTS",
    "PromptTask",
]


class BatchStatus(Enum):
    """
    Enum for batch status.
    """

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    UNKNOWN = "unknown"
