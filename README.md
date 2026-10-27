<div align="center">

# eval-mt

**Machine translation evaluation metrics as a Python library, a CLI and a REST API.**

[![CI](https://github.com/iranailab/eval_mt/actions/workflows/ci.yml/badge.svg)](https://github.com/iranailab/eval_mt/actions/workflows/ci.yml)
[![Release](https://github.com/iranailab/eval_mt/actions/workflows/release.yml/badge.svg)](https://github.com/iranailab/eval_mt/actions/workflows/release.yml)
[![PyPI](https://img.shields.io/pypi/v/evaluation-machine-translation.svg)](https://pypi.org/project/evaluation-machine-translation/)
[![Python](https://img.shields.io/pypi/pyversions/evaluation-machine-translation.svg)](https://pypi.org/project/evaluation-machine-translation/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#license)

[English](README.md) · [فارسی](README.fa.md)

</div>

---

`eval-mt` implements the common metrics for evaluating machine translation from scratch,
with a step-by-step Persian explanation for each one. Version 2 adds:

- 🖥️ **CLI**: `eval-mt score`, `eval-mt corpus`, `eval-mt list`, `eval-mt serve`
- ⚡ **FastAPI server**: a REST API with OpenAPI/Swagger docs
- 🐳 **Docker image** for the API
- ✅ **Tests, Ruff linting and GitHub Actions CI/CD** (PyPI, GHCR, GitHub Releases)

## Metrics

| Metric | Key | Better | References | Docs (Persian) | Code | Colab |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| Tool (n-grams, counters) | – | – | – | [notebook](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/tool.ipynb) | [code](eval_mt/metrics/tool) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uPUFC6E5E5-2A9KVlNGhIIIhfx9-7jH6) |
| BLEU | `bleu` | ↑ | multiple | [notebook](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/bleu.ipynb) | [code](eval_mt/metrics/bleu_score.py) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12ahuWBkulydvlHbyMXK_SMTBxr_H5HCd) |
| NIST | `nist` | ↑ | multiple | [notebook](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/nist.ipynb) | [code](eval_mt/metrics/nist_score.py) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1cCHdi2-hOdT-ZQLtyhRIJ_J2CqUF5V1y) |
| GLEU | `gleu` | ↑ | multiple | [notebook](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/gleu.ipynb) | [code](eval_mt/metrics/gleu_score.py) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tIApcx9RAHll3hMtvEXjwMrx5Z00aUAC) |
| METEOR | `meteor` | ↑ | multiple | [notebook](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/meteor.ipynb) | [code](eval_mt/metrics/meteor_score.py) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XG3UsA_x6_FobK-XxO16UFyVjC6mJ43e) |
| WER | `wer` | ↓ | best of each | [paper](https://dl.acm.org/doi/pdf/10.5555/1289189.1289273) | [code](eval_mt/metrics/wer_score.py) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1DE_UIYWdnKAk56DPfZGd1AK7APCgrGsL?usp=sharing) |
| chrF3 | `chrf` | ↑ | best of each | [notebook](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/chrf.ipynb) | [code](eval_mt/metrics/chrf_score.py) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17Ag-uxviqx24rKElyHXNOpvpv2yb4RWP) |

> chrF and WER compare against one reference. When you pass several, `eval-mt` uses the
> best one: the highest chrF and the lowest WER.

Here are the metrics on 9 sentences from an Iranian machine translation site:

![results](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/assets/89921883/cd03abce-8d67-4fff-aae5-ead8eba8b14f)

## Installation

```bash
# library + CLI
pip install evaluation-machine-translation

# library + CLI + FastAPI server
pip install "evaluation-machine-translation[api]"
```

To install from source:

```bash
git clone https://github.com/iranailab/eval_mt.git
cd eval_mt
pip install -e ".[api,dev]"
```

METEOR uses WordNet. On first use it is downloaded automatically, or you can fetch it ahead of time:

```bash
python -m nltk.downloader wordnet omw-1.4
```

## CLI

```bash
eval-mt --help
eval-mt --version
```

### List metrics

```console
$ eval-mt list
bleu    ↑  BLEU (1-4 gram, brevity penalty)
nist    ↑  NIST (information-weighted n-grams, n=5)
gleu    ↑  Google-BLEU (min of n-gram precision/recall)
meteor  ↑  METEOR (exact, stem and WordNet synonym matches)
chrf    ↑  chrF3 (character 1-6 gram F-score, beta=3)
wer     ↓  Word Error Rate (edit distance / reference length)
```

### Score a sentence

Repeat `-r` to add references and `-m` to choose metrics. Without `-m`, every metric runs.

```console
$ eval-mt score \
    -r "the dog is under the table" \
    -r "a dog is below the table" \
    -H "the dog is under a table"
BLEU    0.5623  ↑
NIST    2.9708  ↑
GLEU    0.6111  ↑
METEOR  0.8519  ↑
CHRF    0.6990  ↑
WER     0.1667  ↓

$ eval-mt score -r "the dog is under the table" -H "the dog is under a table" -m bleu -m wer --json
{
  "bleu": 0.537284965911771,
  "wer": 0.16666666666666666
}
```

### Score a corpus

Files hold one sentence per line, and line *i* of each file belongs to the same sentence.
Repeat `-r` for multiple reference files.

```bash
eval-mt corpus -r refs.en -r refs2.en -H system.en
eval-mt corpus -r refs.en -H system.en -m bleu -m chrf --per-sentence --json > scores.json
```

Corpus scores are the **mean of the sentence-level scores**.

### Start the API

```bash
eval-mt serve --host 0.0.0.0 --port 8000
# or
uvicorn eval_mt.api:app --host 0.0.0.0 --port 8000 --workers 4
```

The CLI exits with `0` on success, `2` on invalid input and `1` when the API extras are missing.

## REST API (FastAPI)

Interactive docs are at **`/docs`** (Swagger UI) and **`/redoc`**.

| Method | Path | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Liveness check and version |
| `GET` | `/v1/metrics` | List available metrics |
| `POST` | `/v1/score` | Score one hypothesis against its references |
| `POST` | `/v1/corpus` | Score a list of aligned sentences |

### `POST /v1/score`

```bash
curl -X POST http://localhost:8000/v1/score \
  -H "Content-Type: application/json" \
  -d '{
        "references": ["the dog is under the table", "a dog is below the table"],
        "hypothesis": "the dog is under a table",
        "metrics": ["bleu", "meteor", "wer"]
      }'
```

```json
{ "scores": { "bleu": 0.5623, "meteor": 0.8519, "wer": 0.1667 } }
```

Leave out `metrics` to compute all of them.

### `POST /v1/corpus`

```bash
curl -X POST http://localhost:8000/v1/corpus \
  -H "Content-Type: application/json" \
  -d '{
        "references": [["the dog is under the table"], ["the cat is on the mat"]],
        "hypotheses": ["the dog is under a table", "the cat is on the mat"],
        "metrics": ["bleu", "chrf"],
        "per_sentence": true
      }'
```

```json
{
  "corpus": { "bleu": 0.7686, "chrf": 0.8495 },
  "sentences": [ { "bleu": 0.5373, "chrf": 0.6990 }, { "bleu": 1.0, "chrf": 1.0 } ]
}
```

Invalid input, such as an unknown metric, an empty hypothesis or mismatched lengths, returns `422`.

### Docker

```bash
docker run -p 8000:8000 ghcr.io/iranailab/eval_mt:latest
# or build it yourself
docker build -t eval-mt .
docker run -p 8000:8000 eval-mt
```

The image runs as a non-root user, includes WordNet and has a built-in health check.

## Python library

```python
from eval_mt import evaluate, evaluate_all, evaluate_corpus

refs = ["the dog is under the table", "a dog is below the table"]
hyp = "the dog is under a table"

evaluate("bleu", refs, hyp)  # 0.5623...
evaluate_all(refs, hyp)  # {"bleu": ..., "nist": ..., ...}
evaluate_all(refs, hyp, ["chrf", "wer"])  # selected metrics only
evaluate_corpus([[r] for r in refs], [hyp, hyp])  # {"corpus": {...}, "sentences": [...]}
```

You can also use the metric classes directly:

```python
from eval_mt.metrics import bleu, chrf, gleu, meteor, nist, wer

bleu(max_n_gram=4).bleu_score(refs, hyp)
chrf().chrf_score(refs[0], hyp)

model = wer()
model.wer_score("the dog is under the table", "The dog is the fable")  # 0.333
model.get_detail()  # {'delete': 0, 'insert': 1, 'substitution': 1, 'same words': 4}
```

## Project layout

```
eval_mt/
├── metrics/          # metric implementations (BLEU, NIST, GLEU, METEOR, WER, chrF)
│   └── tool/         # n-grams, counters, dictionary overlap
├── service.py        # shared entry point used by the library, CLI and API
├── cli.py            # `eval-mt` command
└── api.py            # FastAPI app
tests/                # pytest suite (metrics, CLI, API)
.github/workflows/    # CI and release pipelines
Dockerfile
pyproject.toml
```

## Development

```bash
pip install -e ".[api,dev]"
python -m nltk.downloader wordnet omw-1.4

pytest --cov=eval_mt             # tests + coverage
ruff check .                      # lint
ruff format .                     # format
pre-commit install                # optional: run ruff on every commit
```

## CI/CD

| Workflow | Trigger | What it does |
| :--- | :--- | :--- |
| [`ci.yml`](.github/workflows/ci.yml) | push to `main`, pull requests | Ruff lint and format check → pytest on Python 3.10–3.13 (Linux) plus macOS and Windows → package build and `twine check` → Docker build and API smoke test |
| [`release.yml`](.github/workflows/release.yml) | tag `v*.*.*` | Checks the tag against `__version__` → publishes to **PyPI** (trusted publishing) → pushes a multi-arch image to **GHCR** → creates a **GitHub Release** with the wheels |
| [`dependabot.yml`](.github/dependabot.yml) | weekly | Updates pip, GitHub Actions and Docker dependencies |

**To release**, bump `__version__` in [`eval_mt/__init__.py`](eval_mt/__init__.py), then:

```bash
git tag v2.0.0
git push origin v2.0.0
```

> One-time setup: add a [trusted publisher](https://docs.pypi.org/trusted-publishers/) on PyPI
> for this repository with workflow `release.yml` and environment `pypi`. Also create a GitHub
> environment named `pypi`.

## Migrating from 1.x

| 1.x | 2.x |
| :--- | :--- |
| `from metric.bleu_score import bleu` | `from eval_mt.metrics import bleu` |
| `setup.py` | `pyproject.toml` |
| no CLI or API | `eval-mt` CLI and FastAPI server |

The metric classes and method names are unchanged.

## Contributing

Issues and pull requests are welcome. Run `ruff check .`, `ruff format .` and `pytest`
before opening a PR. CI runs the same checks.

## License

MIT © Alireza Parvaresh
