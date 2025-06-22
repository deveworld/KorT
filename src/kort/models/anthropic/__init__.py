"""
Anthropic Models Module

This module provides access to Anthropic's Claude models for translation
and evaluation tasks within the KorT package.

The module includes:
- Claude model implementation for standard inference
- Claude batch model for batch processing
- Support for various Claude model variants
- API integration with Anthropic's services

Classes:
    ClaudeModel: Standard Claude model for individual requests
    ClaudeBatchModel: Claude model with batch processing capabilities

Both models support the Anthropic API and require appropriate API keys
for authentication. The batch model is optimized for processing large
datasets efficiently.

Example:
    >>> from kort.translators import ModelTranslator
    >>> from kort.data import LangCode
    >>> claude = ModelTranslator("claude", "claude-3-5-haiku-latest", api_key='your-key')
    >>> print(claude.translate("안녕하세요", LangCode.KOR, LangCode.ENG))
    "Hello"
"""

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .claude import ClaudeModel
    from .claude_batch import ClaudeBatchModel

    __all__ = [
        "ClaudeModel",
        "ClaudeBatchModel",
    ]
else:
    from ...utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".claude.ClaudeModel",
        ".claude_batch.ClaudeBatchModel",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
