"""Custom exceptions for KorT."""


class KorTException(Exception):
    """Base exception for KorT."""

    pass


class TranslationError(KorTException):
    """Raised when translation fails."""

    pass


class EvaluationError(KorTException):
    """Raised when evaluation fails."""

    pass


class ModelNotFoundError(KorTException):
    """Raised when a model is not found."""

    pass


class APIKeyError(KorTException):
    """Raised when API key is missing or invalid."""

    pass


class BatchJobError(KorTException):
    """Raised when batch job operations fail."""

    pass


class ConfigurationError(KorTException):
    """Raised when configuration is invalid."""

    pass
