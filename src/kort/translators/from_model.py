from typing import Optional

from ..data import CUSTOM_PROMPTS, PROMPTS, LangCode, PromptTask
from ..models import BaseModel, get_model
from ..translators import BaseTranslator

__all__ = [
    "ModelTranslator",
]


class ModelTranslator(BaseTranslator):
    def __init__(
        self,
        model_type: str,
        model_name: str,
        api_key: Optional[str] = None,
        base_prompt: Optional[str] = None,
        device: Optional[str] = None,
        stop: Optional[str] = None,
    ):
        """
        Initialize the ModelTranslator with a specific model type and name.

        Args:
            model_type (str): The type of the model to use.
            model_name (str): The name of the model to use.
            api_key (str, optional): API key for the model if required. Defaults to None.
            base_prompt (str, optional): The prompt template for translation. Should contain placeholders for text, source_lang, and target_lang.
                Defaults to the translation prompt from PROMPTS.
            device (str, optional): The device to use for the model. Defaults to None.
            stop (str, optional): The stop sequence for the model. Defaults to None.

        Raises:
            ValueError: If the model type is not found or if the model initialization fails.
        """
        self.model_name = model_name
        self.model: BaseModel = get_model(model_type)(
            api_key=api_key, device=device, stop=stop
        )
        if not self.model:
            raise ValueError(f"Model {model_type} not found.")
        self.translator_org = self.model.model_org
        self.translator_name = self.model.model_name
        if base_prompt is None:
            base_prompt = PROMPTS[PromptTask.TRANSLATE]
        else:
            if base_prompt in CUSTOM_PROMPTS.keys():
                base_prompt = CUSTOM_PROMPTS[base_prompt]
        self.base_prompt = base_prompt
        super().__init__()

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
        prompt = self.base_prompt.format(
            text=text,
            source_lang=source_lang.to_iso639_3(),
            target_lang=target_lang.to_iso639_3(),
            source_lang_korean=source_lang.to_korean(),
            target_lang_korean=target_lang.to_korean(),
            source_lang_english=source_lang.to_english(),
            target_lang_english=target_lang.to_english(),
        )

        result = self.model.inference(prompt)
        if not result:
            raise ValueError(f"Translation failed for {self.translator_name}.")

        return result
