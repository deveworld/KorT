import asyncio
import time

from googletrans import Translator

from ...data.lang_code import LangCode
from ...translators.base_translator import BaseTranslator


class GoogleFreeTranslator(BaseTranslator):
    translator_org = "google"
    translator_name = "GoogleTranslateFree"
    _need_api_key = False

    def __init__(self):
        super().__init__(self.translator_name)
        self.translator = Translator()

    def translate(self, text: str, source_lang: LangCode, target_lang: LangCode) -> str:
        """
        Translate the given text from source language to target language using Naver Papago Free API.

        Args:
            text (str): The text to translate.
            source_lang (LangCode): The source language code.
            target_lang (LangCode): The target language code.

        Returns:
            str: The translated text.
        """

        async def async_translate():
            return await self.translator.translate(
                text, src=source_lang.to_iso639_2(), dest=target_lang.to_iso639_2()
            )

        try:
            loop = asyncio.get_event_loop()
            output = loop.run_until_complete(async_translate())
            output = output.text
        except Exception as e:
            print(e)
            if self.error_retry():
                print("Server error, retrying 1 second later...")
                time.sleep(1)
                output = self.translate(text, source_lang, target_lang)
            else:
                print("Server error, stopping...")
                return ""

        if output == "" or output is None:
            if self.error_retry():
                print("Empty output for input, retrying...")
                output = self.translate(text, source_lang, target_lang)
            else:
                print("Error: Empty output for input, stopping...")
                return ""

        output = output.strip().strip("\n")
        return output
