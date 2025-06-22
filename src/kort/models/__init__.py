"""
Models Module for KorT Package

This module provides access to various translation and language models
used for translation generation and evaluation tasks.

The module includes:
- Model discovery and instantiation utilities
- Support for multiple model providers (OpenAI, Anthropic, Google, etc.)
- Batch processing capabilities
- Custom model implementations
- Transformer-based models

Functions:
    get_model: Retrieve model class by type name
    get_all_model_class_names: Get all available model class names
    get_model_list: Get list of regular (non-batch) models
    get_batch_model_list: Get list of batch-capable models

Classes:
    BaseModel: Abstract base class for all models
    BatchModel: Base class for batch-capable models
    All specific model implementations are lazily loaded for performance.

Example:
    >>> from kort.models import get_model, get_model_list
    >>> models = get_model_list()
    >>> openai_model = get_model('openai')('gpt-4', api_key='...')
"""

import sys
from typing import TYPE_CHECKING, Type

from ..utils import _LazyModule
from .base_model import BaseModel


def get_model(model_type: str) -> Type[BaseModel]:
    """
    Get the model class based on the model type name.

    This function supports both lazy-loaded and regular module loading,
    providing a unified interface for model class retrieval.

    Args:
        model_type (str): The type of the model to retrieve.
            Should match the model class name without the 'Model' suffix.
            For example, 'openai' for 'OpenAIModel'.

    Returns:
        Type[BaseModel]: The corresponding model class.

    Raises:
        ValueError: If the specified model type is not found.

    Example:
        >>> model_class = get_model('openai')
        >>> model = model_class('gpt-4', api_key='your-key')
    """
    model_class_name = model_type + "Model"

    # Check if we're using a LazyModule
    module = sys.modules[__name__]
    if isinstance(module, _LazyModule):
        # Check if this model is in the lazy module's attributes
        for attr_name in module._attr_to_module.keys():
            if attr_name.lower() == model_class_name.lower():
                # Access the attribute to trigger lazy loading
                return getattr(module, attr_name)

    # Fall back to original implementation for non-lazy modules or local attributes
    lower_globals = {k.lower(): v for k, v in globals().items()}
    model_class = lower_globals.get(model_class_name.lower())
    if model_class is None:
        raise ValueError(f"Model '{model_type}' not found.")
    return model_class


def get_all_model_class_names() -> list[str]:
    """
    Get a list of all available model class names.

    This function works with both lazy-loaded and regular modules,
    collecting model class names from all available sources.

    Returns:
        list[str]: A list of all available model class names.
            Excludes base classes like 'BaseModel' and 'BatchModel'.

    Example:
        >>> class_names = get_all_model_class_names()
        >>> print(class_names)  # ['OpenAIModel', 'ClaudeModel', ...]
    """
    model_names = []

    # Get models from normal globals
    model_names.extend(
        [
            k
            for k in globals().keys()
            if k not in ["BaseModel", "BatchModel"] and k.endswith("Model")
        ]
    )

    # Check if we're using a LazyModule and add its models
    module = sys.modules[__name__]
    if isinstance(module, _LazyModule):
        # Add models from lazy module's attributes
        model_names.extend(
            [
                attr_name
                for attr_name in module._attr_to_module.keys()
                if attr_name not in ["BaseModel", "BatchModel"]
                and attr_name.endswith("Model")
            ]
        )

    return model_names


def get_model_list() -> list[str]:
    """
    Get a list of available model names (excluding batch models).

    Returns model type names in lowercase, suitable for use with get_model().

    Returns:
        list[str]: A list of available model type names.
            Names are returned in lowercase without the 'Model' suffix.

    Example:
        >>> models = get_model_list()
        >>> print(models)  # ['openai', 'claude', 'gemini', ...]
    """
    return [
        k[:-5].lower()
        for k in get_all_model_class_names()
        if not k.endswith("BatchModel")
    ]


def get_batch_model_list() -> list[str]:
    """
    Get a list of available batch model names.

    Returns batch model type names in lowercase, suitable for batch processing.

    Returns:
        list[str]: A list of available batch model type names.
            Names are returned in lowercase without the 'BatchModel' suffix.

    Example:
        >>> batch_models = get_batch_model_list()
        >>> print(batch_models)  # ['openai', 'claude', ...]
    """
    return [
        k[:-5].lower() for k in get_all_model_class_names() if k.endswith("BatchModel")
    ]


if TYPE_CHECKING:
    from .anthropic import ClaudeBatchModel, ClaudeModel
    from .batch_model import BatchModel
    from .custom import GemagoModel, GugugoModel
    from .google import GeminiModel
    from .openai import OpenAIBatchModel, OpenAIModel
    from .transformer_model import TransformersModel

    __all__ = [
        "BaseModel",
        "BatchModel",
        "ClaudeModel",
        "ClaudeBatchModel",
        "GeminiModel",
        "OpenAIModel",
        "OpenAIBatchModel",
        "TransformersModel",
        "GugugoModel",
        "GemagoModel",
    ]
else:
    _file = globals()["__file__"]
    all_modules = [
        ".anthropic.ClaudeModel",
        ".anthropic.ClaudeBatchModel",
        ".google.GeminiModel",
        ".openai.OpenAIModel",
        ".openai.OpenAIBatchModel",
        ".transformers_model.TransformersModel",
        ".batch_model.BatchModel",
        ".custom.GugugoModel",
        ".custom.GemagoModel",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
