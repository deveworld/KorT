"""
Google Models Module

This module provides access to Google's language models for translation
and evaluation tasks within the KorT package.

The module includes:
- Gemini model implementation
- Integration with Google's AI services
- Support for various Gemini model variants
- API authentication and configuration

Classes:
    GeminiModel: Google's Gemini model for text generation and translation

The Gemini model supports Google's latest language model capabilities
and requires appropriate API credentials for access. It can be used
for both translation generation and evaluation tasks.

Example:
    >>> from kort.translators import ModelTranslator
    >>> from kort.data import LangCode
    >>> gemini = ModelTranslator("gemini", "gemini-2.5-pro", api_key='your-key')
    >>> print(gemini.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
"""

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gemini import GeminiModel

    __all__ = [
        "GeminiModel",
    ]
else:
    from ...utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".gemini.GeminiModel",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
