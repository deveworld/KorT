"""
Leaderboards Module for KorT Package

This module provides leaderboard generation and visualization capabilities
for comparing translation model performance across different metrics and categories.

The module includes:
- Base leaderboard functionality
- Text-based leaderboard display
- Web-based interactive leaderboards
- Model performance summaries
- Data aggregation and ranking utilities

Classes:
    BaseLeaderBoard: Abstract base class for leaderboard implementations
    ModelSummary: Data structure for model performance summaries
    LeaderBoardText: Command-line text-based leaderboard
    LeaderboardWeb: Interactive web-based leaderboard

The leaderboards support multiple evaluation categories, custom sorting,
filtering, and detailed performance breakdowns for comprehensive model comparison.

Example:
    >>> from kort.leaderboards import LeaderboardWeb
    >>> leaderboard = LeaderboardWeb('./evaluated')
    >>> leaderboard.launch()  # Starts web interface
"""

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
