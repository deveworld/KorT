"""
KorT (Korean Translation) Package

A comprehensive toolkit for Korean translation evaluation and benchmarking.
This package provides models, translators, evaluators, and utilities for
working with Korean-English translation tasks.

The package includes:
- Translation models and APIs
- Evaluation frameworks
- Leaderboard generation
- Data processing utilities
- Command-line interfaces

Example:
    Basic usage of the package:
    
    >>> from kort.models import get_model
    >>> from kort.translators import get_translator
    >>> model = get_model('openai')('gpt-4')
    >>> translator = get_translator('papagofree')()
"""
