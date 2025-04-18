from ..data import PROMPTS, LangCode, PromptTask
from ..models import BaseModel, get_model
from ..translators import BaseTranslator


class ModelTranslator(BaseTranslator):
    def __init__(self, model_type: str, model_name: str, api_key: str = None):
        self.model: BaseModel = get_model(model_type)(model_name, api_key=api_key)
        if not self.model:
            raise ValueError(f"Model {model_type} not found.")
        self.translator_org = self.model.model_org
        self.translator_name = self.model.model_name
        super().__init__(self.translator_name)

    def translate(self, text: str, source_lang: LangCode, target_lang: LangCode) -> str:
        """
        Translate the given text from source language to target language using Model.

        Args:
            text (str): The text to translate.
            source_lang (LangCode): The source language code.
            target_lang (LangCode): The target language code.

        Returns:
            str: The translated text.
        """
        prompt = PROMPTS[PromptTask.TRANSLATE].format(
            text=text,
            source_lang=source_lang.to_iso639_3(),
            target_lang=target_lang.to_iso639_3(),
        )

        result = self.model.inference(prompt)
        if not result:
            raise ValueError(f"Translation failed for {self.translator_name}.")

        return result
