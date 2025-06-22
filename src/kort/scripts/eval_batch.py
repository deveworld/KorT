"""
Batch Evaluation Script for KorT Package

This script provides a command-line interface for batch evaluation of translation
models using the KorT framework. It supports batch processing for efficient
evaluation of large datasets using models that support batch inference.

The script handles:
- Batch job submission and management
- Status monitoring for long-running batch jobs
- Result retrieval and processing
- Output formatting and saving

Usage:
    python -m kort.scripts.eval_batch -t MODEL_TYPE -n MODEL_NAME --input INPUT_FILE
    python -m kort.scripts.eval_batch --job_id JOB_ID --input INPUT_FILE

Arguments:
    -t, --model_type: Type of model to use for evaluation
    -n, --model_name: Specific model name/version
    --api_key: API key for model access (if required)
    --input: Path to input JSON file with generated translations
    --output: Path for output evaluation results (optional)
    --job_id: Job ID for retrieving batch results
    -l, --list: List available batch models

Example:
    $ python -m kort.scripts.eval_batch -t openai -n gpt-4 --input generated.json
    $ python -m kort.scripts.eval_batch --job_id batch_123 --input generated.json
"""

import argparse
import json
import os
import time

from ..data import Evaluated, EvaluationMetadata, EvaluationResult, Generated
from ..evaluators import BatchModelEvaluator
from ..models import get_batch_model_list, get_model

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kort Batch Evaluate CLI")
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
    parser.add_argument(
        "--job_id", type=str, help="Job ID for retrieving batch results"
    )

    args = parser.parse_args()

    if args.list:
        print("Available models:")
        for model in get_batch_model_list():
            print(f"- {model}")
        exit(0)
    elif args.model_type is None:
        parser.error("the following arguments are required: --model_type (-t)")
        exit(0)

    model_type = str(args.model_type)
    if model_type in get_batch_model_list():
        print("Using model for evaluator:", model_type)
        evaluator_class = get_model(model_type)
        if args.model_name is None:
            parser.error("the following arguments are required: --model_name (-n)")
            exit(0)
    else:
        print(
            f"Model type '{model_type}' not found. Use --list to see available model types."
        )
        exit(0)

    if evaluator_class._need_api_key:
        if args.api_key is None:
            parser.error("the following arguments are required: --api_key")
            exit(0)
        evaluator = BatchModelEvaluator(
            model_type, args.model_name, api_key=args.api_key
        )
    else:
        evaluator = BatchModelEvaluator(model_type, args.model_name)

    org = evaluator_class.model_org
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

    if not args.job_id:
        batch_id = evaluator.batch_evaluate(generated_data.generated_examples)
        print(f"Batch job ID: {batch_id}")
        exit(0)

    evaluated: list[EvaluationResult] = evaluator.get_batch_result(
        args.job_id, generated_data.generated_examples
    )

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
