import re
import warnings
from typing import Optional, Type

from ..data import PROMPTS, BatchStatus, EvaluationResult, GenerationExample, PromptTask
from ..evaluators import BaseEvaluator
from ..models import BaseModel, BatchModel, get_model


class BatchModelEvaluator(BaseEvaluator):
    def __init__(self, model_type: str, model_name: str, api_key: Optional[str] = None):
        model_class: Type[BaseModel] = get_model(model_type)
        if not issubclass(model_class, BatchModel):
            raise ValueError(
                f"Model {model_class} is not a batch model. Use ModelEvaluator instead."
            )
        self.model: BatchModel = model_class(
            model_name, api_key=api_key, evaluation=True
        )
        if not self.model:
            raise ValueError(f"Model {model_type} not found.")
        self.evaluator_org = self.model.model_org
        self.evaluator_name = self.model.model_name
        super().__init__(self.evaluator_name)

    def batch_evaluate(self, generated_examples: list[GenerationExample]) -> str:
        """
                Evaluate the generated examples in batch.

                Args:
                    generated_examples (list[GenerationExample]): The list of generated examples to evaluate.

                Returns:
                    str: The evaluation result.
        """
        prompts = {}
        for generated in generated_examples:
            prompts[generated.get_hash()] = self.evaluate_prompt(generated)

        id = self.model.batch_inference(prompts)
        if id is None:
            raise ValueError("Batch evaluation failed.")

        return id

    def get_batch_result(
        self, job_id: str, generated_examples: list[GenerationExample]
    ) -> list[EvaluationResult]:
        """
        Get the batch evaluation result.

        Args:
            job_id (str): The id of the batch job.

        Returns:
            list[EvaluationResult]: The list of evaluation results.
        """
        status = self.model.batch_status(job_id)
        if status != BatchStatus.COMPLETED:
            raise ValueError(f"Batch job {job_id} is not completed yet: {status}")

        results = self.model.batch_result(job_id)
        if results is None:
            raise ValueError("Batch result retrieval failed.")

        evaluation_results = []
        for generated in generated_examples:
            hash_id = generated.get_hash()
            if hash_id not in results.keys():
                raise ValueError(f"Batch result for {hash_id} not found.")

            result = results[hash_id]
            evaluation_result = self.parse_result(result, generated)
            evaluation_results.append(evaluation_result)

        if len(evaluation_results) != len(generated_examples):
            warnings.warn(
                f"Batch result length mismatch: {len(evaluation_results)} != {len(generated_examples)}"
                ": it means that some examples are not evaluated."
            )

        return evaluation_results

    def evaluate_prompt(self, generated: GenerationExample) -> str:
        """
        Generate the evaluation prompt for the given generated example.

        Args:
            generated (GenerationExample): The generated example to evaluate.

        Returns:
            str: The evaluation prompt.
        """
        prompt = PROMPTS[PromptTask.EVALUATE].format(
            source_text=generated.source,
            translation_text=generated.translated,
            reference_translation=generated.reference_translation,
            source_lang=generated.source_lang.to_iso639_3(),
            target_lang=generated.target_lang.to_iso639_3(),
        )

        return prompt

    def parse_result(
        self, result: str, generated: GenerationExample
    ) -> EvaluationResult:
        """
        Parse the evaluation result string to extract the score.

        Args:
            result (str): The evaluation result string.
            generated (GenerationExample): The generated example to evaluate.

        Returns:
            EvaluationResult: The evaluation result.
        """
        pattern = r"[-+]?\d*\.?\d+"
        numbers = re.findall(pattern, result)
        if result is None or not numbers:
            raise ValueError(f"Invalid evaluation result format: {result}")

        score = float(numbers[-1].strip().strip("\n"))
        return EvaluationResult(generated=generated, score=score)
