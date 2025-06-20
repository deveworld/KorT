import sys
from typing import TYPE_CHECKING, Type

from ..utils import _LazyModule
from .base_model import BaseModel


def get_model(model_type: str) -> Type[BaseModel]:
    """
    Get the model class based on the model name.

    Args:
        model_name (str): The name of the model to retrieve.

    Returns:
        BaseModel: The corresponding model class.
    """
    model_class_name = model_type + "Model"

    # Check if we're using a LazyModule
    module = sys.modules[__name__]
    if hasattr(module, "_attr_to_module"):
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
    Get a list of all available model names.

    Returns:
        list[str]: A list of all available model names.
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
    if hasattr(module, "_attr_to_module"):
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
    Get a list of available model names. (excluding batch models)

    Returns:
        list[str]: A list of available model names.
    """
    return [
        k[:-5].lower()
        for k in get_all_model_class_names()
        if not k.endswith("BatchModel")
    ]


def get_batch_model_list() -> list[str]:
    """
    Get a list of available batch model names.

    Returns:
        list[str]: A list of available batch model names.
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
