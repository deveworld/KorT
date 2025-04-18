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
