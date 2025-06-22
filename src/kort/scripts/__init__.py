"""
Scripts Module for KorT Package

This module contains command-line interface scripts and utilities
for running various KorT operations from the command line.

The module includes:
- Evaluation scripts for model assessment
- Batch evaluation utilities
- Leaderboard generation scripts
- Data processing and analysis tools

Scripts:
    evaluate.py: Single model evaluation script
    eval_batch.py: Batch model evaluation script
    leaderboard.py: Leaderboard generation and display script

These scripts provide convenient command-line interfaces for common
KorT operations, allowing users to evaluate models, process datasets,
and generate performance reports without writing custom code.

Example:
    Command-line usage:
    $ python -m kort.scripts.generate -t googlefree
    $ python -m kort.scripts.evaluate -t gemini -n gemini-2.5-pro --api_key <your-key> --input generated/google_googletranslatefree.json
    $ python -m kort.scripts.leaderboard -i ./evaluated --text
"""
