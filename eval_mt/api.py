"""HTTP API built with FastAPI. Run with ``eval-mt serve`` or ``uvicorn eval_mt.api:app``."""

from __future__ import annotations

from typing import Dict, List, Literal, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from . import __version__
from .service import METRICS, evaluate_all, evaluate_corpus

MetricName = Literal["bleu", "nist", "gleu", "meteor", "chrf", "wer"]

app = FastAPI(
    title="eval-mt",
    version=__version__,
    description="Machine translation evaluation metrics: BLEU, NIST, GLEU, METEOR, WER and chrF.",
)


class MetricInfo(BaseModel):
    name: str
    description: str
    higher_is_better: bool


class ScoreRequest(BaseModel):
    references: List[str] = Field(..., min_length=1, examples=[["the cat is on the mat"]])
    hypothesis: str = Field(..., min_length=1, examples=["the cat sat on the mat"])
    metrics: Optional[List[MetricName]] = Field(
        None, description="Metrics to compute. Omit to compute all of them."
    )


class ScoreResponse(BaseModel):
    scores: Dict[str, float]


class CorpusRequest(BaseModel):
    references: List[List[str]] = Field(
        ..., min_length=1, description="references[i] holds every reference for hypotheses[i]"
    )
    hypotheses: List[str] = Field(..., min_length=1)
    metrics: Optional[List[MetricName]] = None
    per_sentence: bool = False


class CorpusResponse(BaseModel):
    corpus: Dict[str, float]
    sentences: Optional[List[Dict[str, float]]] = None


@app.get("/health", tags=["meta"])
def health() -> Dict[str, str]:
    return {"status": "ok", "version": __version__}


@app.get("/v1/metrics", response_model=List[MetricInfo], tags=["metrics"])
def list_metrics() -> List[MetricInfo]:
    return [
        MetricInfo(name=m.name, description=m.description, higher_is_better=m.higher_is_better)
        for m in METRICS.values()
    ]


@app.post("/v1/score", response_model=ScoreResponse, tags=["metrics"])
def score(request: ScoreRequest) -> ScoreResponse:
    try:
        return ScoreResponse(scores=evaluate_all(request.references, request.hypothesis, request.metrics))
    except (ValueError, ZeroDivisionError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/v1/corpus", response_model=CorpusResponse, response_model_exclude_none=True, tags=["metrics"])
def corpus(request: CorpusRequest) -> CorpusResponse:
    try:
        result = evaluate_corpus(request.references, request.hypotheses, request.metrics)
    except (ValueError, ZeroDivisionError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return CorpusResponse(
        corpus=result["corpus"], sentences=result["sentences"] if request.per_sentence else None
    )
