import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .base_leaderboard import BaseLeaderBoard, ModelSummary
    from .leaderboard_text import LeaderBoardText
    from .leaderboard_web import LeaderboardWeb

    __all__ = [
        "BaseLeaderBoard",
        "ModelSummary",
        "LeaderBoardText",
        "LeaderboardWeb",
    ]
else:
    from ..utils import _LazyModule

    _file = globals()["__file__"]
    all_modules = [
        ".base_leaderboard.BaseLeaderBoard",
        ".base_leaderboard.ModelSummary",
        ".leaderboard_text.LeaderBoardText",
        ".leaderboard_web.LeaderboardWeb",
    ]
    sys.modules[__name__] = _LazyModule(
        __name__, _file, all_modules, module_spec=__spec__, copy_globals=globals()
    )
