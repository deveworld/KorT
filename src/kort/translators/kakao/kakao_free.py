import time
import uuid

import requests

from ...data.lang_code import LangCode
from ...translators.base_translator import BaseTranslator


class KakaoFreeTranslator(BaseTranslator):
    translator_org = "kakao"
    translator_name = "KakaoFree"
    _need_api_key = False

    def __init__(self):
        super().__init__(self.translator_name)
        self.uvkey = str(uuid.uuid4())
        self.url = f"""https://search.daum.net/qsearch2?mk={self.uvkey}&uk={self.uvkey}&ksk={self.uvkey}&q=kakao+i+%EB%B2%88%EC%97%AD&DA=ESL&m=TR2&w=tot"""

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
        cookies = {"uvkey": self.uvkey}

        headers = {
            "accept": "application/json",
            "accept-language": "ko",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }

        data = {
            "queryLanguage": source_lang.to_iso639_2(),
            "resultLanguage": target_lang.to_iso639_2(),
            "input": text,
        }

        try:
            response = requests.post(
                self.url,
                cookies=cookies,
                headers=headers,
                data=data,
            )
            output = response.json()
            output = output["result"]["output"][0][0]
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
