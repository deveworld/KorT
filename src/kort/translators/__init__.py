from .base_translator import BaseTranslator
from .deepl import DeepLAPITranslator, DeepLFreeTranslator
from .from_model import ModelTranslator
from .naver import PapagoFreeTranslator

__all__ = [
    "BaseTranslator",
    "ModelTranslator",
    "DeepLAPITranslator",
    "DeepLFreeTranslator",
    "PapagoFreeTranslator",
]


def get_translator(translator_name: str) -> BaseTranslator:
    """
    Get the translator class based on the translator name.

    Args:
        translator_name (str): The name of the translator to retrieve.

    Returns:
        BaseTranslator: The corresponding translator class.
    """
    translator_class_name = translator_name + "Translator"
    lower_globals = {k.lower(): v for k, v in globals().items()}
    translator_class = lower_globals.get(translator_class_name.lower())
    if translator_class is None:
        raise ValueError(f"Translator '{translator_name}' not found.")
    return translator_class


def get_translator_list() -> list[str]:
    """
    Get a list of available translator names.

    Returns:
        list[str]: A list of available translator names.
    """
    return [
        k.lower()[:-10]
        for k in globals().keys()
        if k.endswith("Translator") and k != "BaseTranslator" and k != "ModelTranslator"
    ]
