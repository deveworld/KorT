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
