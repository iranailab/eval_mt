"""One entry point for every metric, shared by the Python API, the CLI and the HTTP API."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from typing import Callable, Dict, List, Sequence

from .metrics import bleu, chrf, gleu, meteor, nist, wer


@dataclass(frozen=True)
class Metric:
    name: str
    description: str
    higher_is_better: bool
    compute: Callable[[Sequence[str], str], float]


def _ensure_wordnet() -> None:
    import nltk

    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet", quiet=True)
        nltk.download("omw-1.4", quiet=True)


def _meteor(refs: Sequence[str], hyp: str) -> float:
    _ensure_wordnet()
    return meteor().metor_score(list(refs), hyp)


# chrF and WER are single-reference metrics: with several references we keep the best match.
METRICS: Dict[str, Metric] = {
    "bleu": Metric(
        "bleu", "BLEU (1-4 gram, brevity penalty)", True, lambda refs, hyp: bleu().bleu_score(list(refs), hyp)
    ),
    "nist": Metric(
        "nist",
        "NIST (information-weighted n-grams, n=5)",
        True,
        lambda refs, hyp: nist().nist_score(list(refs), hyp),
    ),
    "gleu": Metric(
        "gleu",
        "Google-BLEU (min of n-gram precision/recall)",
        True,
        lambda refs, hyp: gleu().gleu_score(list(refs), hyp),
    ),
    "meteor": Metric("meteor", "METEOR (exact, stem and WordNet synonym matches)", True, _meteor),
    "chrf": Metric(
        "chrf",
        "chrF3 (character 1-6 gram F-score, beta=3)",
        True,
        lambda refs, hyp: max(chrf().chrf_score(ref, hyp) for ref in refs),
    ),
    "wer": Metric(
        "wer",
        "Word Error Rate (edit distance / reference length)",
        False,
        lambda refs, hyp: min(float(wer().wer_score(ref, hyp)) for ref in refs),
    ),
}


def _validate(metric: str, references: Sequence[str], hypothesis: str) -> Metric:
    if metric not in METRICS:
        raise ValueError(f"Unknown metric '{metric}'. Available: {', '.join(METRICS)}")
    if not references or not all(ref.strip() for ref in references):
        raise ValueError("At least one non-empty reference is required.")
    if not hypothesis.strip():
        raise ValueError("Hypothesis must not be empty.")
    return METRICS[metric]


def evaluate(metric: str, references: Sequence[str], hypothesis: str) -> float:
    """Score one hypothesis against one or more references with a single metric."""
    return float(_validate(metric, references, hypothesis).compute(references, hypothesis))


def evaluate_all(
    references: Sequence[str], hypothesis: str, metrics: Sequence[str] | None = None
) -> Dict[str, float]:
    """Score one hypothesis with several metrics (all of them by default)."""
    return {name: evaluate(name, references, hypothesis) for name in (metrics or list(METRICS))}


def evaluate_corpus(
    references: Sequence[Sequence[str]], hypotheses: Sequence[str], metrics: Sequence[str] | None = None
) -> Dict[str, object]:
    """Score aligned sentence pairs; returns per-sentence scores and their mean per metric.

    ``references[i]`` holds every reference for ``hypotheses[i]``.
    """
    if len(references) != len(hypotheses):
        raise ValueError(f"Got {len(references)} reference sets but {len(hypotheses)} hypotheses.")
    if not hypotheses:
        raise ValueError("Corpus is empty.")
    sentences: List[Dict[str, float]] = [
        evaluate_all(refs, hyp, metrics) for refs, hyp in zip(references, hypotheses, strict=True)
    ]
    names = list(sentences[0])
    return {
        "corpus": {name: mean(scores[name] for scores in sentences) for name in names},
        "sentences": sentences,
    }
