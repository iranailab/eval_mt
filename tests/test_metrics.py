import pytest

from eval_mt import METRICS, evaluate, evaluate_all, evaluate_corpus
from eval_mt.metrics import bleu, chrf, gleu, nist, wer

REF = "the dog is under the table"


def test_identical_sentences_score_perfectly():
    scores = evaluate_all([REF], REF, ["bleu", "gleu", "chrf", "wer"])
    assert scores["bleu"] == pytest.approx(1.0)
    assert scores["gleu"] == pytest.approx(1.0)
    assert scores["chrf"] == pytest.approx(1.0)
    assert scores["wer"] == pytest.approx(0.0)


def test_better_translation_scores_higher():
    good = "the dog is under a table"
    bad = "a cat sits near some chair"
    for name in ("bleu", "gleu", "chrf", "nist"):
        assert evaluate(name, [REF], good) > evaluate(name, [REF], bad), name
    assert evaluate("wer", [REF], good) < evaluate("wer", [REF], bad)


def test_short_hypothesis_does_not_crash():
    assert bleu().bleu_score([REF], "the dog") >= 0
    assert nist().nist_score([REF], "the dog") >= 0


def test_wer_details():
    model = wer()
    score = model.wer_score(REF, "The dog is the fable")
    assert score == pytest.approx(2 / 6)
    detail = model.get_detail()
    assert detail["same words"] == 4


def test_wer_details_with_extra_words_terminates():
    model = wer()
    model.wer_score("a b", "a b c d")
    assert sum(model.get_detail().values()) >= 2


def test_chrf_example_from_docstring():
    assert chrf().chrf_score("this is a blue ball", "this iss a blue bal") > 0.7


def test_gleu_multiple_references_takes_best():
    assert gleu().gleu_score(["something else entirely", REF], REF) == pytest.approx(1.0)


def test_meteor():
    pytest.importorskip("nltk")
    assert evaluate("meteor", [REF], REF) > 0.9
    assert evaluate("meteor", [REF], REF) > evaluate("meteor", [REF], "a cat sits near some chair")


def test_unknown_metric():
    with pytest.raises(ValueError, match="Unknown metric"):
        evaluate("rouge", [REF], REF)


@pytest.mark.parametrize("refs, hyp", [([], "x"), ([""], "x"), ([REF], "  ")])
def test_invalid_input(refs, hyp):
    with pytest.raises(ValueError):
        evaluate("bleu", refs, hyp)


def test_corpus():
    result = evaluate_corpus([[REF], [REF]], [REF, "the dog is under a table"], ["bleu", "wer"])
    assert set(result["corpus"]) == {"bleu", "wer"}
    assert len(result["sentences"]) == 2
    assert result["corpus"]["bleu"] == pytest.approx(
        (result["sentences"][0]["bleu"] + result["sentences"][1]["bleu"]) / 2
    )


def test_corpus_length_mismatch():
    with pytest.raises(ValueError):
        evaluate_corpus([[REF]], [REF, REF])


def test_registry_is_complete():
    assert set(METRICS) == {"bleu", "nist", "gleu", "meteor", "chrf", "wer"}
