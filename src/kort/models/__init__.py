from .anthropic import ClaudeBatchModel, ClaudeModel
from .base_model import BaseModel
from .batch_model import BatchModel
from .google import GeminiModel
from .openai import OpenAIBatchModel, OpenAIModel
from .transformer_model import TransformersModel

__all__ = [
    "BaseModel",
    "BatchModel",
    "GeminiModel",
    "OpenAIModel",
    "OpenAIBatchModel",
    "ClaudeModel",
    "ClaudeBatchModel",
    "TransformersModel",
]


def get_model(model_type: str) -> BaseModel:
    """
    Get the model class based on the model name.

    Args:
        model_name (str): The name of the model to retrieve.

    Returns:
        BaseModel: The corresponding model class.
    """
    model_class_name = model_type + "Model"
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
    return [
        k
        for k in globals().keys()
        if k not in ["BaseModel", "BatchModel"] and k.endswith("Model")
    ]


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
