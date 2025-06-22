"""
OpenAI Models Module

This module provides access to OpenAI's language models for translation
and evaluation tasks within the KorT package.

The module includes:
- OpenAI GPT model implementation for standard inference
- OpenAI batch model for batch processing
- Support for various GPT model variants (GPT-3.5, GPT-4, etc.)
- API integration with OpenAI's services

Classes:
    OpenAIModel: Standard OpenAI model for individual requests
    OpenAIBatchModel: OpenAI model with batch processing capabilities

Both models support the OpenAI API and require appropriate API keys
for authentication. The batch model is optimized for processing large
datasets efficiently and cost-effectively.

Example:
    >>> from kort.translators import ModelTranslator
    >>> from kort.data import LangCode
    >>> openai = ModelTranslator("openai", "gpt-4.1", api_key='your-key')
    >>> print(openai.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
"""

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .gpt import OpenAIModel
    from .gpt_batch import OpenAIBatchModel

    __all__ = [
        "OpenAIModel",
        "OpenAIBatchModel",
    ]
else:
    from ...utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".gpt.OpenAIModel",
        ".gpt_batch.OpenAIBatchModel",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
