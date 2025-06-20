import time

import deepl

from ...data.lang_code import LangCode
from ...translators.base_translator import BaseTranslator


class DeepLAPITranslator(BaseTranslator):
    translator_org = "DeepL"
    translator_name = "DeepLAPI"
    _need_api_key = True

    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.translator = deepl.DeepLClient(self.api_key)

    def translate(self, text: str, source_lang: LangCode, target_lang: LangCode) -> str:
        """
        Translate the given text from source language to target language using DeeL Free API.

        Args:
            text (str): The text to translate.
            source_lang (LangCode): The source language code.
            target_lang (LangCode): The target language code.

        Returns:
            str: The translated text.
        """
        target_lang_upper = target_lang.to_iso639_2().upper()
        if target_lang_upper == "EN":
            target_lang_upper = "EN-US"

        try:
            result = self.translator.translate_text(
                text,
                source_lang=source_lang.to_iso639_2().upper(),
                target_lang=target_lang_upper,
            )
            if isinstance(result, list):
                output = result[0].text if result else ""
            else:
                output = result.text
        except Exception as e:
            print(e)
            if self.error_retry():
                print("Server error, retrying 1 second later...")
                time.sleep(1)
                output = self.translate(text, source_lang, target_lang)
            else:
                print(f"Error: {self.error} times, stopping...")
                return ""

        if output == "" or output is None:
            if self.error_retry():
                print("Empty output for input, retrying...")
                output = self.translate(text, source_lang, target_lang)
            else:
                print(f"Error: {self.error} times, stopping...")
                return ""

        output = output.strip().strip("\n")
        return output
