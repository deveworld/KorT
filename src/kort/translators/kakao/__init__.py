"""
Kakao Translators Module

This module provides access to Kakao translation services for Korean-English
translation tasks within the KorT package.

The module includes:
- Kakao Free translator for web-based translation
- Specialized support for Korean language translation
- Integration with Kakao's translation services

Classes:
    KakaoFreeTranslator: Free Kakao translation service

Kakao provides translation services with particular strength in Korean
language processing, making it well-suited for Korean-English translation
tasks within the KorT framework.

Example:
    >>> from kort.data import LangCode
    >>> from kort.translators.kakao import KakaoFreeTranslator
    >>> translator = KakaoFreeTranslator()
    >>> print(translator.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
"""

import sys
from typing import TYPE_CHECKING

from ...utils import _LazyModule

if TYPE_CHECKING:
    from .kakao_free import KakaoFreeTranslator

    __all__ = [
        "KakaoFreeTranslator",
    ]
else:
    _file = globals()["__file__"]
    all_modules = [
        ".kakao_free.KakaoFreeTranslator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
