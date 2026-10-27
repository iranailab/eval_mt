<div dir="rtl">

# eval-mt — ارزیابی ترجمه ماشینی

[![CI](https://github.com/iranailab/eval_mt/actions/workflows/ci.yml/badge.svg)](https://github.com/iranailab/eval_mt/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/evaluation-machine-translation.svg)](https://pypi.org/project/evaluation-machine-translation/)

[English](README.md) · [فارسی](README.fa.md)

این کتابخانه معیارهای رایج ارزیابی ترجمه ماشینی را از صفر پیاده‌سازی کرده است. برای هر معیار هم یک نوت‌بوک
آموزشی به فارسی وجود دارد. در **نسخه ۲**:

- 🖥️ **رابط خط فرمان (CLI)**: دستور `eval-mt`
- ⚡ **API با FastAPI** به همراه مستندات Swagger
- 🐳 **ایمیج Docker** برای API
- ✅ **تست، Ruff و CI/CD در GitHub Actions** (انتشار خودکار روی PyPI، GHCR و GitHub Releases)

## معیارها

| معیار | کلید | بهتر | مستند فارسی | کولب |
| :---: | :---: | :---: | :---: | :---: |
| BLEU | `bleu` | ↑ | [نوت‌بوک](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/bleu.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12ahuWBkulydvlHbyMXK_SMTBxr_H5HCd) |
| NIST | `nist` | ↑ | [نوت‌بوک](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/nist.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1cCHdi2-hOdT-ZQLtyhRIJ_J2CqUF5V1y) |
| GLEU | `gleu` | ↑ | [نوت‌بوک](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/gleu.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1tIApcx9RAHll3hMtvEXjwMrx5Z00aUAC) |
| METEOR | `meteor` | ↑ | [نوت‌بوک](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/meteor.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1XG3UsA_x6_FobK-XxO16UFyVjC6mJ43e) |
| WER | `wer` | ↓ | [مقاله](https://dl.acm.org/doi/pdf/10.5555/1289189.1289273) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1DE_UIYWdnKAk56DPfZGd1AK7APCgrGsL?usp=sharing) |
| chrF3 | `chrf` | ↑ | [نوت‌بوک](https://github.com/parvvaresh/Evaluation-of-machine-translation-by-NLP/blob/main/duc-fa/chrf.ipynb) | [![Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/17Ag-uxviqx24rKElyHXNOpvpv2yb4RWP) |

ستون «بهتر» جهت بهتر شدن امتیاز را نشان می‌دهد. ↑ یعنی بیشتر بهتر است و ↓ (مثل WER) یعنی کمتر بهتر است.
chrF و WER هر بار با یک مرجع مقایسه می‌کنند. اگر چند مرجع بدهید، بهترین نتیجه گزارش می‌شود.

## نصب

</div>

```bash
pip install evaluation-machine-translation          # کتابخانه + CLI
pip install "evaluation-machine-translation[api]"   # + سرور FastAPI
python -m nltk.downloader wordnet omw-1.4           # برای METEOR (اختیاری؛ خودکار هم دانلود می‌شود)
```

<div dir="rtl">

## خط فرمان (CLI)

</div>

```bash
eval-mt list                                   # فهرست معیارها
eval-mt score -r "the dog is under the table" -H "the dog is under a table"
eval-mt score -r "ref 1" -r "ref 2" -H "hyp" -m bleu -m wer --json
eval-mt corpus -r refs.txt -H hyps.txt --per-sentence     # هر خط یک جمله
eval-mt serve --host 0.0.0.0 --port 8000       # اجرای API
```

<div dir="rtl">

- با `-r` مرجع می‌دهید. برای چند مرجع، آن را تکرار کنید.
- با `-H` ترجمه ماشین (فرضیه) را می‌دهید.
- با `-m` معیارها را انتخاب می‌کنید. اگر `-m` را ندهید، همه معیارها محاسبه می‌شوند.
- با `--json` خروجی JSON می‌گیرید.

## API (FastAPI)

بعد از اجرای سرور، مستندات تعاملی در `http://localhost:8000/docs` در دسترس است.

| متد | مسیر | توضیح |
| :---: | :--- | :--- |
| `GET` | `/health` | وضعیت سرویس |
| `GET` | `/v1/metrics` | فهرست معیارها |
| `POST` | `/v1/score` | امتیاز یک جمله |
| `POST` | `/v1/corpus` | امتیاز مجموعه‌ای از جمله‌ها |

</div>

```bash
curl -X POST http://localhost:8000/v1/score \
  -H "Content-Type: application/json" \
  -d '{"references": ["the dog is under the table"], "hypothesis": "the dog is under a table", "metrics": ["bleu", "wer"]}'
# {"scores": {"bleu": 0.5373, "wer": 0.1667}}
```

<div dir="rtl">

### Docker

</div>

```bash
docker run -p 8000:8000 ghcr.io/iranailab/eval_mt:latest
```

<div dir="rtl">

## استفاده در پایتون

</div>

```python
from eval_mt import evaluate, evaluate_all

evaluate("bleu", ["the dog is under the table"], "the dog is under a table")
evaluate_all(["the dog is under the table"], "the dog is under a table")
```

<div dir="rtl">

## توسعه و CI/CD

</div>

```bash
pip install -e ".[api,dev]"
pytest --cov=eval_mt
ruff check . && ruff format .
pre-commit install
```

<div dir="rtl">

- **CI** (`ci.yml`): با هر push و pull request اجرا می‌شود و این مراحل را انجام می‌دهد:
  - بررسی کد با Ruff
  - تست روی پایتون ۳٫۱۰ تا ۳٫۱۳ و روی لینوکس، مک و ویندوز
  - ساخت پکیج
  - ساخت ایمیج Docker و تست API
- **CD** (`release.yml`): با push کردن تگی مثل `v2.0.0` اجرا می‌شود و این کارها را انجام می‌دهد:
  - انتشار روی PyPI
  - انتشار ایمیج روی GHCR
  - ساخت GitHub Release

</div>

```bash
git tag v2.0.0 && git push origin v2.0.0
```

<div dir="rtl">

## مجوز

MIT © علیرضا پرورش

</div>
