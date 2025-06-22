"""
DeepL Translators Module

This module provides access to DeepL translation services for Korean-English
translation tasks within the KorT package.

The module includes:
- DeepL API translator for paid API access
- DeepL Free translator for free web-based translation
- Support for high-quality neural machine translation
- Rate limiting and error handling

Classes:
    DeepLAPITranslator: Official DeepL API translator (requires API key)
    DeepLFreeTranslator: Free DeepL web translator (no API key required)

DeepL is known for producing high-quality translations, particularly
for European languages. The API version provides more reliable access
and higher rate limits compared to the free web version.

Example:
    >>> from kort.data import LangCode
    >>> from kort.translators.deepl import DeepLAPITranslator, DeepLFreeTranslator
    >>> translator = DeepLAPITranslator(api_key='your-key')
    >>> free_translator = DeepLFreeTranslator()
    >>> print(translator.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
    >>> print(free_translator.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
"""

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .deepl_api import DeepLAPITranslator
    from .deepl_free import DeepLFreeTranslator

    __all__ = [
        "DeepLAPITranslator",
        "DeepLFreeTranslator",
    ]
else:
    from ...utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".deepl_api.DeepLAPITranslator",
        ".deepl_free.DeepLFreeTranslator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
