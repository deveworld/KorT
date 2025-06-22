from abc import ABC, abstractmethod
from typing import Optional

from ..config import translation_config
from ..data import LangCode
from ..utils.exceptions import APIKeyError, TranslationError
from ..utils.retry import retry_with_backoff


class BaseTranslator(ABC):
    """
    Base class for all translators.
    """

    translator_org: str = "BaseTranslator"
    translator_name: str = "BaseTranslator"
    _need_api_key: bool = False
    error = 0

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the base translator with the specified translator name and API key.

        Args:
            api_key: The API key for accessing the translator. Defaults to None.

        Raises:
            TranslationError: If BaseTranslator is instantiated directly.
            APIKeyError: If API key is required but not provided.
        """
        if self.translator_org == "BaseTranslator":
            raise TranslationError("BaseTranslator cannot be instantiated directly.")

        if self._need_api_key and api_key is None:
            raise APIKeyError("API key is required for this translator.")

        if api_key is not None:
            self.api_key = api_key

    @abstractmethod
    def translate(self, text: str, source_lang: LangCode, target_lang: LangCode) -> str:
        """
        Translate the given text from source language to target language.

        Args:
            text: The text to translate.
            source_lang: The source language code.
            target_lang: The target language code.

        Returns:
            The translated text.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Translate method not implemented.")

    def error_retry(self) -> bool:
        """
        Handle error retry logic.

        Returns:
            True if should retry, False if should stop.
        """
        self.error = self.error if self.error else 0
        self.error += 1

        if self.error > translation_config.max_retries:
            print(f"Error: {self.error} times, stopping...")
            self.error = 0
            return False
        return True

    @retry_with_backoff(max_retries=3, base_delay=1.0)
    def safe_translate(
        self, text: str, source_lang: LangCode, target_lang: LangCode
    ) -> str:
        """
        Translate with automatic retry on failure.

        Args:
            text: The text to translate.
            source_lang: The source language code.
            target_lang: The target language code.

        Returns:
            The translated text.
        """
        return self.translate(text, source_lang, target_lang)
