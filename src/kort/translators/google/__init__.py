"""
Google Translators Module

This module provides access to Google translation services for Korean-English
translation tasks within the KorT package.

The module includes:
- Google Free translator for web-based translation
- Support for Google's neural machine translation
- Automatic language detection capabilities
- Rate limiting and error handling

Classes:
    GoogleFreeTranslator: Free Google Translate web service

Google Translate provides broad language support and is widely used
for general translation tasks. The free version has usage limitations
but is suitable for development and testing purposes.

Example:
    >>> from kort.data import LangCode
    >>> from kort.translators.google import GoogleFreeTranslator
    >>> translator = GoogleFreeTranslator()
    >>> print(translator.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
"""

import sys
from typing import TYPE_CHECKING

from ...utils import _LazyModule

if TYPE_CHECKING:
    from .google_free import GoogleFreeTranslator

    __all__ = [
        "GoogleFreeTranslator",
    ]
else:
    _file = globals()["__file__"]
    all_modules = [
        ".google_free.GoogleFreeTranslator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
