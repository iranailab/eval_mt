"""Evaluation metrics for machine translation (BLEU, NIST, GLEU, METEOR, WER, chrF)."""

from .service import METRICS, evaluate, evaluate_all, evaluate_corpus

__version__ = "2.0.0"

__all__ = ["METRICS", "evaluate", "evaluate_all", "evaluate_corpus", "__version__"]
