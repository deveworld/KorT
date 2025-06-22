"""
Generation Script for KorT Package

This script provides a command-line interface for generating translations
using various translation models and services within the KorT framework.

The script handles:
- Model and translator discovery and instantiation
- Translation generation across multiple language pairs
- Support for both API-based and local models
- Custom prompt templates and configurations
- Output formatting and saving

Usage:
    python -m kort.scripts.generate -t TRANSLATOR_TYPE [OPTIONS]

Arguments:
    -t, --model_type: Type of translator/model to use
    -n, --model_name: Specific model name (required for model-based translation)
    --api_key: API key for model access (if required)
    --output: Path for output translation results (optional)
    -p, --prompt_type: Custom prompt template to use
    -d, --device: Device to use for local models (e.g., 'cuda', 'cpu')
    -s, --stop: Stop sequence for generation
    -l, --list: List available translators and models

The script automatically processes all evaluation data from EVAL_DATA,
generating translations for each example and saving results in a structured format.

Example:
    $ python -m kort.scripts.generate -t papagofree
    $ python -m kort.scripts.generate -t openai -n gpt-4 --api_key your-key
    $ python -m kort.scripts.generate -t gugugo -n squarelike/Gugugo-koen-7B-V1.1 -d cuda
"""

import argparse
import os
import time
from typing import Type

import tqdm

from ..data import EVAL_DATA, Generated, GenerationExample, GenerationMetadata, LangCode
from ..models import BaseModel, get_model, get_model_list
from ..translators import (
    BaseTranslator,
    ModelTranslator,
    get_translator,
    get_translator_list,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kort Generate CLI")
    parser.add_argument("-t", "--model_type", type=str, help="Model type")
    parser.add_argument(
        "-n", "--model_name", type=str, help="Model name (if applicable)"
    )
    parser.add_argument("--api_key", type=str, help="API key for the model")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument(
        "-p", "--prompt_type", type=str, help="Prompt type for the model"
    )
    parser.add_argument("-d", "--device", type=str, help="Device to use for the model")
    parser.add_argument("-s", "--stop", type=str, help="Stop sequence for the model")
    parser.add_argument(
        "-l", "--list", action="store_true", help="List available model types"
    )

    args = parser.parse_args()

    if args.list:
        print("Available models:")
        for model in get_model_list() + get_translator_list():
            print(f"- {model}")
        exit(0)
    elif args.model_type is None:
        parser.error("the following arguments are required: --model")
        exit(0)

    model_type = str(args.model_type)
    translator_class: Type[BaseTranslator] | Type[BaseModel]
    if model_type in get_translator_list():
        print("Using native translator:", model_type)
        translator_class = get_translator(model_type)
    elif model_type in get_model_list():
        print("Using model for translator:", model_type)
        translator_class = get_model(model_type)
        if args.model_name is None:
            parser.error("the following arguments are required: --model_name")
            exit(0)
    else:
        print(
            f"Model type '{model_type}' not found. Use --list to see available model types."
        )
        exit(0)

    prompt = args.prompt_type
    device = args.device
    stop = args.stop
    translator: BaseTranslator | ModelTranslator
    if translator_class._need_api_key:
        if args.api_key is None:
            parser.error("the following arguments are required: --api_key")
            exit(0)
        if issubclass(translator_class, BaseTranslator):
            translator = translator_class(api_key=args.api_key)
        else:
            translator = ModelTranslator(
                model_type,
                args.model_name,
                api_key=args.api_key,
                base_prompt=prompt,
                device=device,
                stop=stop,
            )
    else:
        if issubclass(translator_class, BaseTranslator):
            translator = translator_class()
        else:
            translator = ModelTranslator(
                model_type,
                args.model_name,
                base_prompt=prompt,
                device=device,
                stop=stop,
            )

    org = translator.translator_org
    name = translator.translator_name
    output = args.output
    if output is None:
        output = f"generated/{org.lower()}_{name.lower()}.json"

    print("Output file:", output)
    if os.path.exists(output):
        print(f"Output file {output} already exists. Please choose a different name.")
        exit(0)

    print(f"Using {org} {model_type} - {name}")
    os.makedirs(os.path.dirname(output), exist_ok=True)

    def invert_ko_en(code: LangCode) -> LangCode:
        """
        Invert Korean-English language codes.
        
        Args:
            code: Language code to invert (KOR or ENG)
            
        Returns:
            Inverted language code
            
        Raises:
            ValueError: If language code is not KOR or ENG
        """
        if code == LangCode.KOR:
            return LangCode.ENG
        elif code == LangCode.ENG:
            return LangCode.KOR
        else:
            raise ValueError(
                f"Unsupported language code for inversion: {code}. Only KOR and ENG are supported."
            )

    generated = []
    for source_lang, categories in tqdm.tqdm(
        EVAL_DATA.items(), desc="Language", leave=False
    ):
        for category, examples in tqdm.tqdm(
            categories.items(), desc="Category", leave=False
        ):
            for example in tqdm.tqdm(examples, desc="Sentence", leave=False):
                text = example.source
                translated_text = translator.translate(
                    text, source_lang, invert_ko_en(source_lang)
                )
                generated.append(
                    GenerationExample(
                        source=text,
                        translated=translated_text,
                        source_lang=source_lang,
                        target_lang=invert_ko_en(source_lang),
                        category=category,
                        reference_translation=example.translation[
                            invert_ko_en(source_lang)
                        ],
                    )
                )

    data = Generated(
        metadata=GenerationMetadata(
            model_type=model_type,
            model_name=name,
            model_org=org,
            timestamp=str(time.time() * 1000),
        ),
        generated_examples=generated,
    )
    with open(output, "w", encoding="utf-8") as f:
        f.write(data.model_dump_json(indent=2))

    print(f"Generated data saved to {output}")
