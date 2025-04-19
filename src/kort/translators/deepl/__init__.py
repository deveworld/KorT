import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .deepl_api import DeepLAPITranslator
    from .deepl_free import DeepLFreeTranslator

    __all__ = [
        "DeepLAPITranslator",
        "DeepLFreeTranslator",
    ]
else:
    from ...utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".deepl_api.DeepLAPITranslator",
        ".deepl_free.DeepLFreeTranslator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
