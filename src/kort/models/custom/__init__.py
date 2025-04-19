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
