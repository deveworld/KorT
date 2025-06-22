"""
Evaluation Script for KorT Package

This script provides a command-line interface for evaluating translation
models using the KorT framework. It supports both native evaluators and
model-based evaluation approaches.

The script handles:
- Model and evaluator discovery and instantiation
- Input data validation and processing
- Evaluation execution with progress tracking
- Results aggregation and output formatting

Usage: 
    python -m kort.scripts.evaluate -t MODEL_TYPE [OPTIONS]

Arguments:
    -t, --model_type: Type of model/evaluator to use
    -n, --model_name: Specific model name (required for model-based evaluation)
    --api_key: API key for model access (if required)
    --input: Path to input JSON file with generated translations
    --output: Path for output evaluation results (optional)
    -l, --list: List available models and evaluators

The script automatically detects whether to use a native evaluator or
model-based evaluation based on the specified model type.

Example:
    $ python -m kort.scripts.evaluate -t human --input generated.json
    $ python -m kort.scripts.evaluate -t openai -n gpt-4 --input generated.json
"""

import argparse
import json
import os
import time
from typing import Type

import tqdm

from ..data import Evaluated, EvaluationMetadata, EvaluationResult, Generated
from ..evaluators import (
    BaseEvaluator,
    ModelEvaluator,
    get_evaluator,
    get_evaluator_list,
)
from ..models import BaseModel, get_model, get_model_list

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kort Evaluate CLI")
    parser.add_argument("-t", "--model_type", type=str, help="Model type")
    parser.add_argument(
        "-n", "--model_name", type=str, help="Model name (if applicable)"
    )
    parser.add_argument("--api_key", type=str, help="API key for the model")
    parser.add_argument("--input", type=str, help="Input file path")
    parser.add_argument("--output", type=str, help="Output file path")
    parser.add_argument(
        "-l", "--list", action="store_true", help="List available model types"
    )

    args = parser.parse_args()

    if args.list:
        print("Available models:")
        for model in get_model_list() + get_evaluator_list():
            print(f"- {model}")
        exit(0)
    elif args.model_type is None:
        parser.error("the following arguments are required: --model")
        exit(0)

    model_type = str(args.model_type)
    evaluator_class: type[BaseEvaluator] | Type[BaseModel]
    if model_type in get_evaluator_list():
        print("Using native evaluator:", model_type)
        evaluator_class = get_evaluator(model_type)
    elif model_type in get_model_list():
        print("Using model for evaluator:", model_type)
        evaluator_class = get_model(model_type)
        if args.model_name is None:
            parser.error("the following arguments are required: --model_name")
            exit(0)
    else:
        print(
            f"Model type '{model_type}' not found. Use --list to see available model types."
        )
        exit(0)

    evaluator: BaseEvaluator | ModelEvaluator
    if evaluator_class._need_api_key:
        if args.api_key is None:
            parser.error("the following arguments are required: --api_key")
            exit(0)
        if issubclass(evaluator_class, BaseEvaluator):
            evaluator = evaluator_class(api_key=args.api_key)
        else:
            evaluator = ModelEvaluator(
                model_type, args.model_name, api_key=args.api_key
            )
    else:
        if issubclass(evaluator_class, BaseEvaluator):
            evaluator = evaluator_class()
        else:
            evaluator = ModelEvaluator(model_type, args.model_name)

    org = evaluator.evaluator_org
    name = args.model_name if args.model_name else "N/A"
    print(f"Using {org} {model_type} - {name}")
    if args.input is None:
        parser.error("the following arguments are required: --input")
        exit(0)

    input_file = args.input
    output_file = args.output
    if output_file is None:
        output_file = (
            "evaluated/"
            + os.path.basename(os.path.splitext(input_file)[0])
            + "_evaluation.json"
        )

    if os.path.exists(output_file):
        print(
            f"Output file '{output_file}' already exists. Please remove it or specify a different output file."
        )
        exit(0)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    try:
        with open(input_file, "r") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading input file '{input_file}': {e}")
        exit(0)

    try:
        generated_data = Generated.model_validate(data)
    except Exception as e:
        print(f"Error validating input data: {e}")
        exit(0)
    item_count = len(generated_data.generated_examples)
    print(f"Loaded {item_count} generated data item(s) from `{input_file}`")
    if item_count < 1:
        print(f"Input file '{input_file}' is empty or invalid.")
        exit(0)

    evaluated: list[EvaluationResult] = []
    for example in tqdm.tqdm(generated_data.generated_examples):
        result = evaluator.evaluate(example)
        evaluated.append(result)

    mean_score = sum([result.score for result in evaluated]) / len(evaluated)
    print(f"Mean score: {mean_score:.2f}")
    data = Evaluated(
        metadata=EvaluationMetadata(
            eval_model_type=model_type,
            eval_model_name=name,
            eval_model_org=org,
            gen_model_type=generated_data.metadata.model_type,
            gen_model_name=generated_data.metadata.model_name,
            gen_model_org=generated_data.metadata.model_org,
            timestamp=str(time.time() * 1000),
            mean_score=mean_score,
        ),
        evaluation_results=evaluated,
    )
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(data.model_dump_json(indent=2))

    print(f"Evaluation data saved to {output_file}")
