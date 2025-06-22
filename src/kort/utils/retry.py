"""Retry utilities for KorT."""

import logging
import time
from functools import wraps
from typing import Callable, TypeVar

from .exceptions import KorTException

T = TypeVar("T")

logger = logging.getLogger(__name__)


def retry_with_backoff(
    max_retries: int = 5,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Decorator for retrying functions with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        backoff_factor: Multiplier for delay after each retry
        exceptions: Tuple of exceptions to catch and retry on
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            last_exception = None

            func_name = getattr(func, "__name__", repr(func))
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt == max_retries:
                        logger.error(
                            f"Function {func_name} failed after {max_retries} retries: {e}"
                        )
                        raise

                    delay = base_delay * (backoff_factor**attempt)
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func_name}: {e}. Retrying in {delay:.1f}s..."
                    )
                    time.sleep(delay)

            # This should never be reached, but just in case
            raise last_exception or KorTException(
                f"Function {func_name} failed unexpectedly"
            )

        return wrapper

    return decorator
