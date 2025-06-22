"""
Custom Models Module

This module provides custom model implementations specifically designed
for Korean translation tasks within the KorT package.

The module includes:
- Gugugo model: Custom Korean translation model
- Gemago model: Alternative Korean translation model
- Specialized configurations for Korean language processing
- Custom prompt templates and processing logic

Classes:
    GugugoModel: Custom Korean translation model implementation
    GemagoModel: Alternative Korean translation model implementation

These models are specifically tuned for Korean-English translation tasks
and may use custom tokenization, prompting strategies, or fine-tuned
weights optimized for Korean language processing.

Example:
    >>> from kort.translators import ModelTranslator
    >>> from kort.data import LangCode
    >>> gugugo = ModelTranslator("gugugo", "squarelike/Gugugo-koen-7B-V1.1")
    >>> gemago = ModelTranslator("gemago", "devworld/Gemago-2b")
    >>> print(gugugo.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
    >>> print(gemago.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
"""

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gemago import GemagoModel
    from .gugugo import GugugoModel

    __all__ = [
        "GemagoModel",
        "GugugoModel",
    ]
else:
    from ...utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".gugugo.GugugoModel",
        ".gemago.GemagoModel",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
