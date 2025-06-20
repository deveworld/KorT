from pydantic import BaseModel

from .generate import GenerationExample


class EvaluationResult(BaseModel):
    """
    Evaluation result for a single example.
    """

    generated: GenerationExample
    score: float


class EvaluationMetadata(BaseModel):
    eval_model_type: str
    eval_model_name: str
    eval_model_org: str

    gen_model_type: str
    gen_model_name: str
    gen_model_org: str

    timestamp: str
    mean_score: float


class Evaluated(BaseModel):
    metadata: EvaluationMetadata
    evaluation_results: list[EvaluationResult]
