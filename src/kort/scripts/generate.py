import argparse
import os
import time

import tqdm

from ..data import EVAL_DATA, Generated, GeneratedExample, GenerationMetadata, LangCode
from ..models import get_model, get_model_list
from ..translators import ModelTranslator, get_translator, get_translator_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kort Generate CLI")
    parser.add_argument("-t", "--model_type", type=str, help="Model type")
    parser.add_argument(
        "-n", "--model_name", type=str, help="Model name (if applicable)"
    )
    parser.add_argument("--api_key", type=str, help="API key for the model")
    parser.add_argument("--output", type=str, help="Output file path")
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
    is_native = False
    if model_type in get_translator_list():
        print("Using native translator:", model_type)
        translator_class = get_translator(model_type)
        is_native = True
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

    if translator_class._need_api_key:
        if args.api_key is None:
            parser.error("the following arguments are required: --api_key")
            exit(0)
        if is_native:
            translator = translator_class(api_key=args.api_key)
        else:
            translator = ModelTranslator(
                model_type, args.model_name, api_key=args.api_key
            )
    else:
        if is_native:
            translator = translator_class()
        else:
            translator = ModelTranslator(model_type, args.model_name)

    org = translator_class.translator_org if is_native else translator_class.model_org
    name = args.model_name if args.model_name else translator_class.translator_name
    output = args.output
    if output is None:
        output = f"generated/{org.lower()}_{name.lower()}.json"

    if os.path.exists(output):
        print(f"Output file {output} already exists. Please choose a different name.")
        exit(0)

    print(f"Using {org} {model_type} - {name}")
    os.makedirs(os.path.dirname(output), exist_ok=True)

    def invert_ko_en(code: LangCode) -> LangCode:
        if code == LangCode.KOR:
            return LangCode.ENG
        elif code == LangCode.ENG:
            return LangCode.KOR

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
                    GeneratedExample(
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
