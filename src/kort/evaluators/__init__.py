"""
Evaluators Module for KorT Package

This module provides evaluation frameworks and utilities for assessing
translation quality and model performance.

The module includes:
- Base evaluator classes
- Model-based evaluators
- Batch evaluation support
- Human evaluation interfaces
- Evaluator discovery and instantiation utilities

Functions:
    get_evaluator: Retrieve evaluator class by name
    get_evaluator_list: Get list of available evaluators

Classes:
    All evaluator classes are lazily loaded for performance.

Example:
    >>> from kort.evaluators import get_evaluator, get_evaluator_list
    >>> evaluators = get_evaluator_list()
    >>> human_eval = get_evaluator('human')()
"""

import sys
from typing import TYPE_CHECKING, Type

from ..utils import _LazyModule
from .base_evaluator import BaseEvaluator


def get_evaluator(evaluator_name: str) -> Type[BaseEvaluator]:
    """
    Get the evaluator class based on the evaluator name.

    This function supports both lazy-loaded and regular module loading,
    providing a unified interface for evaluator class retrieval.

    Args:
        evaluator_name (str): The name of the evaluator to retrieve.
            Should match the evaluator class name without the 'Evaluator' suffix.
            For example, 'human' for 'HumanEvaluator'.

    Returns:
        Type[BaseEvaluator]: The corresponding evaluator class.

    Raises:
        ValueError: If the specified evaluator is not found.

    Example:
        >>> evaluator_class = get_evaluator('human')
        >>> evaluator = evaluator_class()
    """
    evaluator_class_name = evaluator_name + "Evaluator"

    # Check if we're using a LazyModule
    module = sys.modules[__name__]
    if isinstance(module, _LazyModule):
        # Check if this model is in the lazy module's attributes
        for attr_name in module._attr_to_module.keys():
            if attr_name.lower() == evaluator_class_name.lower():
                # Access the attribute to trigger lazy loading
                return getattr(module, attr_name)

    lower_globals = {k.lower(): v for k, v in globals().items()}
    evaluator_class = lower_globals.get(evaluator_class_name.lower())
    if evaluator_class is None:
        raise ValueError(f"Evaluator '{evaluator_name}' not found.")
    return evaluator_class


def get_evaluator_list() -> list[str]:
    """
    Get a list of available evaluator names.

    This function works with both lazy-loaded and regular modules,
    collecting evaluator names from all available sources.

    Returns:
        list[str]: A list of available evaluator names (without 'Evaluator' suffix).
            Names are returned in lowercase for consistency.

    Example:
        >>> evaluators = get_evaluator_list()
        >>> print(evaluators)  # ['human', 'model', ...]
    """
    evaluator_name = []

    # Get models from normal globals
    evaluator_name.extend(
        [
            k
            for k in globals().keys()
            if k not in ["BaseEvaluator", "ModelEvaluator", "BatchModelEvaluator"]
            and k.endswith("Evaluator")
        ]
    )

    # Check if we're using a LazyModule and add its models
    module = sys.modules[__name__]
    if isinstance(module, _LazyModule):
        # Add models from lazy module's attributes
        evaluator_name.extend(
            [
                attr_name
                for attr_name in module._attr_to_module.keys()
                if attr_name
                not in ["BaseEvaluator", "ModelEvaluator", "BatchModelEvaluator"]
                and attr_name.endswith("Evaluator")
            ]
        )

    return evaluator_name


if TYPE_CHECKING:
    from .from_batch import BatchModelEvaluator
    from .from_model import ModelEvaluator
    from .human import HumanEvaluator

    __all__ = [
        "BatchModelEvaluator",
        "ModelEvaluator",
        "HumanEvaluator",
        "get_evaluator",
        "get_evaluator_list",
    ]
else:
    _file = globals()["__file__"]
    all_modules = [
        ".from_batch.BatchModelEvaluator",
        ".from_model.ModelEvaluator",
        ".human.HumanEvaluator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
