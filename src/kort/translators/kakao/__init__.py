import sys
from typing import TYPE_CHECKING

from ...utils import _LazyModule

if TYPE_CHECKING:
    from .kakao_free import KakaoFreeTranslator

    __all__ = [
        "KakaoFreeTranslator",
    ]
else:
    _file = globals()["__file__"]
    all_modules = [
        ".kakao_free.KakaoFreeTranslator",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
