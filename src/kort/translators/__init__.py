"""
Translators Module for KorT Package

This module provides access to various translation services and APIs
for Korean-English translation tasks within the KorT package.

The module includes:
- Translation service discovery and instantiation utilities
- Support for multiple translation providers (Google, Naver, DeepL, Kakao)
- Model-based translation using language models
- Free and paid API integrations

Functions:
    get_translator: Retrieve translator class by name
    get_translator_list: Get list of available translators

Classes:
    BaseTranslator: Abstract base class for all translators
    ModelTranslator: Translator using language models
    All specific translator implementations are lazily loaded for performance.

The module supports both free and commercial translation services,
allowing users to choose the most appropriate option for their needs.

Example:
    >>> from kort.data import LangCode
    >>> from kort.translators import get_translator, get_translator_list
    >>> translators = get_translator_list()
    >>> papago = get_translator('papagofree')()
    >>> result = papago.translate('Hello', LangCode.ENG, LangCode.KOR)
"""

import sys
from typing import TYPE_CHECKING, Type

from ..utils import _LazyModule
from .base_translator import BaseTranslator


def get_translator(translator_name: str) -> Type[BaseTranslator]:
    """
    Get the translator class based on the translator name.

    This function supports both lazy-loaded and regular module loading,
    providing a unified interface for translator class retrieval.

    Args:
        translator_name (str): The name of the translator to retrieve.
            Should match the translator class name without the 'Translator' suffix.
            For example, 'papagofree' for 'PapagoFreeTranslator'.

    Returns:
        Type[BaseTranslator]: The corresponding translator class.

    Raises:
        ValueError: If the specified translator is not found.

    Example:
        >>> translator_class = get_translator('papagofree')
        >>> translator = translator_class()
    """
    translator_class_name = translator_name + "Translator"

    # Check if we're using a LazyModule
    module = sys.modules[__name__]
    if isinstance(module, _LazyModule):
        # Check if this translator is in the lazy module's attributes
        for attr_name in module._attr_to_module.keys():
            if attr_name.lower() == translator_class_name.lower():
                # Access the attribute to trigger lazy loading
                return getattr(module, attr_name)

    # Fall back to original implementation for non-lazy modules or local attributes
    lower_globals = {k.lower(): v for k, v in globals().items()}
    translator_class = lower_globals.get(translator_class_name.lower())
    if translator_class is None:
        raise ValueError(f"Translator '{translator_name}' not found.")
    return translator_class


def get_translator_list() -> list[str]:
    """
    Get a list of available translator names.

    This function works with both lazy-loaded and regular modules,
    collecting translator names from all available sources.

    Returns:
        list[str]: A list of available translator names (without 'Translator' suffix).
            Names are returned in lowercase for consistency.
            Excludes base classes like 'BaseTranslator' and 'ModelTranslator'.

    Example:
        >>> translators = get_translator_list()
        >>> print(translators)  # ['papagofree', 'googlefree', 'deeplapi', ...]
    """
    # This version works with _LazyModule by checking module's internal state
    module = sys.modules[__name__]

    if isinstance(module, _LazyModule):
        translator_names = []

        # Get translators from normal globals
        translator_names.extend(
            [
                k.lower()[:-10]
                for k in globals().keys()
                if k.endswith("Translator")
                and k != "BaseTranslator"
                and k != "ModelTranslator"
            ]
        )

        # Get translators from lazy module
        for attr_name in module._attr_to_module.keys():
            if (
                attr_name.endswith("Translator")
                and attr_name != "BaseTranslator"
                and attr_name != "ModelTranslator"
            ):
                translator_names.append(attr_name.lower()[:-10])

        return translator_names
    else:
        # Original implementation for when not using _LazyModule
        return [
            k.lower()[:-10]
            for k in globals().keys()
            if k.endswith("Translator")
            and k != "BaseTranslator"
            and k != "ModelTranslator"
        ]


if TYPE_CHECKING:
    from .deepl import DeepLAPITranslator, DeepLFreeTranslator
    from .from_model import ModelTranslator
    from .google import GoogleFreeTranslator
    from .kakao import KakaoFreeTranslator
    from .naver import PapagoFreeTranslator

    __all__ = [
        "BaseTranslator",
        "ModelTranslator",
        "DeepLAPITranslator",
        "DeepLFreeTranslator",
        "PapagoFreeTranslator",
        "GoogleFreeTranslator",
        "KakaoFreeTranslator",
    ]
else:
    _file = globals()["__file__"]
    all_modules = [
        ".base_translator.BaseTranslator",
        ".from_model.ModelTranslator",
        ".deepl.DeepLAPITranslator",
        ".deepl.DeepLFreeTranslator",
        ".naver.PapagoFreeTranslator",
        ".google.GoogleFreeTranslator",
        ".kakao.KakaoFreeTranslator",
    ]

    # Create lazy module with our modified functions
    lazy_module = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )

    # Replace the module
    sys.modules[__name__] = lazy_module
