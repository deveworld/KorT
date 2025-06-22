import base64
import hashlib
import hmac
import time
import uuid

import requests

from ...data.lang_code import LangCode
from ...translators.base_translator import BaseTranslator


class PapagoFreeTranslator(BaseTranslator):
    translator_org = "Naver"
    translator_name = "PapagoFree"
    _need_api_key = False

    def __init__(self):
        super().__init__(self.translator_name)
        self.url = "https://papago.naver.com/apis/n2mt/translate"
        self.key = "v1.8.9_a5c5d7faee"
        self.device_id = ""
        self.timestamp = ""
        self.authorization = ""
        self.refresh_token()

    def refresh_token(self):
        self.device_id = str(uuid.uuid4())
        self.timestamp = str(int(time.time() * 1000))

        message = f"{self.device_id}\n{self.url}\n{self.timestamp}"
        hmac_md5 = hmac.new(self.key.encode(), message.encode(), hashlib.md5)
        encoded = base64.b64encode(hmac_md5.digest()).decode(encoding="UTF-8")
        self.authorization = f"PPG {self.device_id}:{encoded}"

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
        headers = {
            "accept": "application/json",
            "accept-language": "ko",
            "authorization": self.authorization,
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "timestamp": self.timestamp,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        }

        data = {
            "deviceId": self.device_id,
            "locale": "ko",
            "dict": "false",
            "honorific": "false",
            "instant": "false",
            "paging": "false",
            "source": source_lang.to_iso639_2(),
            "target": target_lang.to_iso639_2(),
            "text": text,
            "usageAgreed": "false",
        }

        try:
            response = requests.post(
                "https://papago.naver.com/apis/n2mt/translate",
                cookies={},
                headers=headers,
                data=data,
            )
            output = response.json()["translatedText"]
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
