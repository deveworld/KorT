import sys
from typing import TYPE_CHECKING

from ..utils import _LazyModule
from .base_translator import BaseTranslator


def get_translator(translator_name: str) -> BaseTranslator:
    """
    Get the translator class based on the translator name.

    Args:
        translator_name (str): The name of the translator to retrieve.

    Returns:
        BaseTranslator: The corresponding translator class.
    """
    translator_class_name = translator_name + "Translator"

    # Check if we're using a LazyModule
    module = sys.modules[__name__]
    if hasattr(module, "_attr_to_module"):
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

    Returns:
        list[str]: A list of available translator names.
    """
    # This version works with _LazyModule by checking module's internal state
    module = sys.modules[__name__]

    # If this is a _LazyModule, use its attribute mapping
    if hasattr(module, "_attr_to_module"):
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
    from .naver import PapagoFreeTranslator
    from .google import GoogleFreeTranslator
    from .kakao import KakaoFreeTranslator

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
