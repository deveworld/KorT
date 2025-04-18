from pydantic import BaseModel

from .generate import GeneratedExample


class EvaluationResult(BaseModel):
    """
    Evaluation result for a single example.
    """

    generated: GeneratedExample
    score: int


class EvaluationMetadata(BaseModel):
    model_type: str
    model_name: str
    model_org: str
    timestamp: str
    mean_score: float


class Evaluated(BaseModel):
    metadata: EvaluationMetadata
    evaluation_results: list[EvaluationResult]
