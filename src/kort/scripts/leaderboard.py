"""
Leaderboard Script for KorT Package

This script provides a command-line interface for generating and displaying
leaderboards based on evaluation results from the KorT framework.

The script supports:
- Text-based leaderboard display for command-line viewing
- Web-based interactive leaderboard with filtering and sorting
- Automatic data loading from evaluation result directories
- Multiple display formats and customization options

Usage:
    python -m kort.scripts.leaderboard [OPTIONS]

Arguments:
    -t, --text: Display leaderboard in text format (default: web interface)
    -i, --input: Input directory containing evaluation results

The script automatically discovers and loads all evaluation result files
from the specified directory, aggregates the results, and presents them
in a ranked leaderboard format.

Example:
    $ python -m kort.scripts.leaderboard -i ./evaluated --text
    $ python -m kort.scripts.leaderboard -i ./results  # Web interface
"""

import argparse
import os

from ..leaderboards import LeaderBoardText, LeaderboardWeb

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kort LeaderBoard CLI")
    parser.add_argument(
        "-t", "--text", action="store_true", help="View leaderboard in text"
    )
    parser.add_argument("-i", "--input", type=str, help="Input directory path")

    args = parser.parse_args()

    input_dir = args.input
    if input_dir is None:
        input_dir = "./evaluated"
        print("Input directory not provided. Using default: ./evaluated")

    if not os.path.exists(input_dir):
        print(f"Input directory '{input_dir}' does not exist.")
        exit(1)

    if args.text:
        leaderboard = LeaderBoardText(input_dir)
    else:
        leaderboard = LeaderboardWeb(input_dir)

    leaderboard.launch()
