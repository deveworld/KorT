"""
Data Module for KorT Package

This module provides data structures, enums, and utilities for handling
translation and evaluation data within the KorT package.

The module includes:
- BatchStatus enum for tracking batch job states
- Evaluation data models (Evaluated, EvaluationResult, EvaluationMetadata)
- Generation data models (Generated, GenerationExample, GenerationMetadata)
- Language code definitions (LangCode)
- Prompt templates and configurations
- Evaluation datasets (EVAL_DATA)

Classes:
    BatchStatus: Enum for batch processing status tracking
    
Data:
    All data models and utilities are lazily loaded for performance.

Example:
    >>> from kort.data import BatchStatus, LangCode
    >>> status = BatchStatus.COMPLETED
    >>> lang = LangCode.KOR
"""

import sys
from enum import Enum
from typing import TYPE_CHECKING


class BatchStatus(Enum):
    """
    Enum for batch status.
    
    Used to track the status of batch processing jobs across different
    model providers and evaluation systems.
    
    Attributes:
        IN_PROGRESS: Job is currently being processed
        COMPLETED: Job has finished successfully
        FAILED: Job encountered an error and failed
        UNKNOWN: Job status cannot be determined
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
