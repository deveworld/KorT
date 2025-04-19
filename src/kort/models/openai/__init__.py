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
