from typing import Optional

from ..data import LangCode


class BaseTranslator:
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
            translator_name (str): The name of the translator to initialize.
            api_key (str, optional): The API key for accessing the translator. Defaults to None.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if self.translator_org == "BaseTranslator":
            raise ValueError("BaseTranslator cannot be instantiated directly.")

        if self._need_api_key and api_key is None:
            raise ValueError("API key is required for this translator.")
        if api_key is not None:
            self.api_key = api_key

    def translate(self, text: str, source_lang: LangCode, target_lang: LangCode) -> str:
        """
        Translate the given text from source language to target language.

        Args:
            text (str): The text to translate.
            source_lang (LangCode): The source language code.
            target_lang (LangCode): The target language code.

        Returns:
            str: The translated text.
        """
        raise NotImplementedError("Translate method not implemented.")

    def error_retry(self) -> bool:
        self.error = self.error if self.error else 0
        self.error += 1
        if self.error > 5:
            print(f"Error: {self.error} times, stopping...")
            self.error = 0
            return False
        return True
