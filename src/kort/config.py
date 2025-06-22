"""Configuration management for KorT."""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class APIConfig:
    """Configuration for API services."""

    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    google_api_key: Optional[str] = None
    deepl_api_key: Optional[str] = None

    def __post_init__(self):
        """Load from environment variables if not provided."""
        self.openai_api_key = self.openai_api_key or os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = self.anthropic_api_key or os.getenv(
            "ANTHROPIC_API_KEY"
        )
        self.google_api_key = self.google_api_key or os.getenv("GOOGLE_API_KEY")
        self.deepl_api_key = self.deepl_api_key or os.getenv("DEEPL_API_KEY")


@dataclass
class EvaluationConfig:
    """Configuration for evaluation settings."""

    max_retries: int = 5
    retry_delay: float = 1.0
    timeout: int = 30
    max_tokens: int = 8192
    evaluation_max_tokens: int = 16512


@dataclass
class TranslationConfig:
    """Configuration for translation settings."""

    max_retries: int = 5
    retry_delay: float = 1.0
    timeout: int = 30
    max_length: int = 8192


# Global configuration instance
config = APIConfig()
eval_config = EvaluationConfig()
translation_config = TranslationConfig()
