import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .human import HumanEvaluator

    __all__ = [
        "HumanEvaluator",
    ]
else:
    from ...utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".human.HumanEvaluator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
