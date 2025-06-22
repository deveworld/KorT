"""
Utilities Module for KorT Package

This module provides utility functions and classes used throughout
the KorT package for various common operations.

The module includes:
- Lazy module loading utilities for performance optimization
- Import management and dynamic loading
- Common helper functions and decorators

Classes:
    _LazyModule: Lazy loading implementation for modules

The lazy loading system helps improve package startup time by deferring
the import of heavy dependencies until they are actually needed.

Example:
    >>> from kort.utils import _LazyModule
    >>> # Used internally for lazy loading of modules
"""

from .import_utils import _LazyModule

__all__ = [
    "_LazyModule",
]
