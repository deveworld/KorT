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
