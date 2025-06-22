"""
Human Evaluator Module

This module provides human evaluation interfaces for translation quality assessment.
Human evaluation is considered the gold standard for translation quality assessment,
providing subjective quality scores that automated metrics may miss.

Classes:
    HumanEvaluator: Interactive human evaluation interface

The HumanEvaluator class provides a command-line interface for human annotators
to evaluate translation quality, typically used as a reference standard for
comparing automated evaluation metrics.

Example:
    >>> from kort.evaluators.human import HumanEvaluator
    >>> evaluator = HumanEvaluator()
    >>> result = evaluator.evaluate(translation_example)
"""

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .human import HumanEvaluator

    __all__ = [
        "HumanEvaluator",
    ]
else:
    from ...utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".human.HumanEvaluator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
