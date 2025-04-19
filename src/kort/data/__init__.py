import sys
from enum import Enum
from typing import TYPE_CHECKING


class BatchStatus(Enum):
    """
    Enum for batch status.
    """

    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    UNKNOWN = "unknown"


if TYPE_CHECKING:
    from .evaluate import (
        Evaluated,
        EvaluationMetadata,
        EvaluationResult,
    )
    from .generate import (
        EVAL_DATA,
        Categories,
        Example,
        Generated,
        GenerationExample,
        GenerationMetadata,
    )
    from .lang_code import LangCode
    from .prompts import (
        CUSTOM_PROMPTS,
        PROMPTS,
        PromptTask,
    )

    __all__ = [
        "BatchStatus",
        "Evaluated",
        "EvaluationMetadata",
        "EvaluationResult",
        "EVAL_DATA",
        "Categories",
        "Example",
        "Generated",
        "GenerationExample",
        "GenerationMetadata",
        "LangCode",
        "CUSTOM_PROMPTS",
        "PROMPTS",
        "PromptTask",
    ]
else:
    from ..utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".evaluate.Evaluated",
        ".evaluate.EvaluationMetadata",
        ".evaluate.EvaluationResult",
        ".generate.EVAL_DATA",
        ".generate.Categories",
        ".generate.Example",
        ".generate.Generated",
        ".generate.GenerationExample",
        ".generate.GenerationMetadata",
        ".lang_code.LangCode",
        ".prompts.PROMPTS",
        ".prompts.CUSTOM_PROMPTS",
        ".prompts.PromptTask",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
