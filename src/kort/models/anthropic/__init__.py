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
