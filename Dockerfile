# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build
WORKDIR /src
COPY pyproject.toml README.md ./
COPY eval_mt ./eval_mt
RUN pip install --no-cache-dir build && python -m build --wheel --outdir /dist

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    NLTK_DATA=/usr/share/nltk_data
COPY --from=build /dist/*.whl /tmp/
RUN pip install --no-cache-dir --default-timeout=120 "$(ls /tmp/*.whl)[api]" && rm /tmp/*.whl \
    && python -m nltk.downloader -d "$NLTK_DATA" wordnet omw-1.4 \
    && useradd --create-home --uid 1000 app
USER app
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "eval_mt.api:app", "--host", "0.0.0.0", "--port", "8000"]
