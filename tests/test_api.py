import pytest

pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from eval_mt import __version__  # noqa: E402
from eval_mt.api import app  # noqa: E402

client = TestClient(app)
REF = "the dog is under the table"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}


def test_list_metrics():
    response = client.get("/v1/metrics")
    assert response.status_code == 200
    assert {m["name"] for m in response.json()} == {"bleu", "nist", "gleu", "meteor", "chrf", "wer"}


def test_score():
    response = client.post(
        "/v1/score", json={"references": [REF], "hypothesis": REF, "metrics": ["bleu", "wer"]}
    )
    assert response.status_code == 200
    assert response.json()["scores"] == pytest.approx({"bleu": 1.0, "wer": 0.0})


def test_score_unknown_metric_is_rejected():
    response = client.post("/v1/score", json={"references": [REF], "hypothesis": REF, "metrics": ["rouge"]})
    assert response.status_code == 422


def test_score_empty_hypothesis_is_rejected():
    response = client.post("/v1/score", json={"references": [REF], "hypothesis": "   "})
    assert response.status_code == 422


def test_corpus():
    response = client.post(
        "/v1/corpus",
        json={
            "references": [[REF], [REF]],
            "hypotheses": [REF, "the dog is under a table"],
            "metrics": ["bleu"],
            "per_sentence": True,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["sentences"]) == 2
    assert 0 < body["corpus"]["bleu"] < 1


def test_corpus_without_sentences():
    response = client.post(
        "/v1/corpus", json={"references": [[REF]], "hypotheses": [REF], "metrics": ["chrf"]}
    )
    assert response.status_code == 200
    assert "sentences" not in response.json()
