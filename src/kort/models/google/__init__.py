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
