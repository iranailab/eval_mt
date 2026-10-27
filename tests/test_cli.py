import json

import pytest

from eval_mt import __version__
from eval_mt.cli import main

REF = "the dog is under the table"


def run(capsys, *argv):
    code = main(list(argv))
    out, err = capsys.readouterr()
    return code, out, err


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_list(capsys):
    code, out, _ = run(capsys, "list", "--json")
    assert code == 0
    assert "bleu" in json.loads(out)


def test_score_json(capsys):
    code, out, _ = run(capsys, "score", "-r", REF, "-H", REF, "-m", "bleu", "-m", "wer", "--json")
    assert code == 0
    assert json.loads(out) == pytest.approx({"bleu": 1.0, "wer": 0.0})


def test_score_table(capsys):
    code, out, _ = run(capsys, "score", "-r", REF, "-H", "the dog is under a table", "-m", "chrf")
    assert code == 0
    assert out.startswith("CHRF")


def test_corpus(tmp_path, capsys):
    refs = tmp_path / "refs.txt"
    hyps = tmp_path / "hyps.txt"
    refs.write_text(f"{REF}\n{REF}\n", encoding="utf-8")
    hyps.write_text(f"{REF}\nthe dog is under a table\n", encoding="utf-8")
    code, out, _ = run(
        capsys, "corpus", "-r", str(refs), "-H", str(hyps), "-m", "bleu", "--per-sentence", "--json"
    )
    assert code == 0
    data = json.loads(out)
    assert len(data["sentences"]) == 2
    assert 0 < data["corpus"]["bleu"] < 1


def test_corpus_line_mismatch(tmp_path, capsys):
    refs = tmp_path / "refs.txt"
    hyps = tmp_path / "hyps.txt"
    refs.write_text("a b c\n", encoding="utf-8")
    hyps.write_text("a b c\nd e f\n", encoding="utf-8")
    code, _, err = run(capsys, "corpus", "-r", str(refs), "-H", str(hyps))
    assert code == 2
    assert "error" in err


def test_bad_input_returns_error_code(capsys):
    code, _, err = run(capsys, "score", "-r", REF, "-H", " ")
    assert code == 2
    assert "error" in err
