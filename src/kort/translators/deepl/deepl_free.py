import http.client
import json
import random
import time
import uuid

from ...data.lang_code import LangCode
from ...translators.base_translator import BaseTranslator


class DeepLFreeTranslator(BaseTranslator):
    translator_org = "DeepL"
    translator_name = "DeepLFree"
    _need_api_key = False

    def __init__(self):
        super().__init__(self.translator_name)
        self.url = "www2.deepl.com"
        self.post = "/jsonrpc?method=LMT_handle_jobs"

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
        conn = http.client.HTTPSConnection("www2.deepl.com")
        headers = {
            "accept": "*/*",
            "accept-language": "ko-KR,ko;q=0.9",
            "content-type": "application/json",
            "dnt": "1",
            "origin": "https://www.deepl.com",
            "priority": "u=1, i",
            "referer": "https://www.deepl.com/",
            "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
            "cookie": f"userCountry=KR; verifiedBot=false; dapUid={uuid.uuid4()}",
        }
        json_data = {
            "jsonrpc": "2.0",
            "method": "LMT_handle_jobs",
            "params": {
                "jobs": [
                    {
                        "kind": "default",
                        "sentences": [
                            {
                                "text": text,
                                "id": 1,
                                "prefix": "",
                            },
                        ],
                        "raw_en_context_before": [],
                        "raw_en_context_after": [],
                        "preferred_num_beams": 4,
                    },
                ],
                "lang": {
                    "target_lang": target_lang.to_iso639_2().upper(),
                    "preference": {
                        "weight": {},
                        "default": "default",
                    },
                    "source_lang_computed": source_lang.to_iso639_2().upper(),
                },
                "priority": -1,
                "commonJobParams": {
                    "quality": "normal",
                    "mode": "translate",
                    "browserType": 1,
                    "textType": "plaintext",
                },
                "timestamp": int(time.time() * 1000),
            },
            "id": random.randrange(1_000_000, 100_000_000),
        }

        try:
            conn.request(
                "POST",
                "/jsonrpc?method=LMT_handle_jobs",
                json.dumps(json_data),
                headers,
            )
            response = conn.getresponse()
            res = response.read().decode("utf-8")
            conn.close()
            output = json.loads(res)["result"]["translations"][0]["beams"][0][
                "sentences"
            ][0]["text"]
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
