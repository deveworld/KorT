"""
Naver Translators Module

This module provides access to Naver translation services for Korean-English
translation tasks within the KorT package.

The module includes:
- Papago Free translator for web-based translation
- Specialized support for Korean language translation
- Integration with Naver's Papago translation service

Classes:
    PapagoFreeTranslator: Free Naver Papago translation service

Naver Papago is particularly strong for Korean language translation,
being developed by a Korean company with deep understanding of Korean
linguistics and cultural context.

Example:
    >>> from kort.data import LangCode
    >>> from kort.translators.naver import PapagoFreeTranslator
    >>> translator = PapagoFreeTranslator()
    >>> print(translator.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
"""

import sys
from typing import TYPE_CHECKING

from ...utils import _LazyModule

if TYPE_CHECKING:
    from .papago_free import PapagoFreeTranslator

    __all__ = [
        "PapagoFreeTranslator",
    ]
else:
    _file = globals()["__file__"]
    all_modules = [
        ".papago_free.PapagoFreeTranslator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
