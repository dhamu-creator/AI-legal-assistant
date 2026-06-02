"""Evaluation module for legal assistant"""

from .evaluator import (
    EvaluationQuestion,
    LegalAnswer,
    CitationAccuracyResult,
    FaithfulnessResult,
    RelevanceResult,
    CompleteLegalEvaluation,
    CitationEvaluator,
    FaithfulnessEvaluator,
    RelevanceEvaluator,
    LegalAssistantEvaluator,
)

__all__ = [
    "EvaluationQuestion",
    "LegalAnswer",
    "CitationAccuracyResult",
    "FaithfulnessResult",
    "RelevanceResult",
    "CompleteLegalEvaluation",
    "CitationEvaluator",
    "FaithfulnessEvaluator",
    "RelevanceEvaluator",
    "LegalAssistantEvaluator",
]
