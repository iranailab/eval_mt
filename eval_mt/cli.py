"""Command line interface: ``eval-mt``."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from . import __version__
from .service import METRICS, evaluate_all, evaluate_corpus


def _metric_list(values: Optional[List[str]]) -> List[str]:
    if not values or "all" in values:
        return list(METRICS)
    return values


def _print_scores(scores: Dict[str, float]) -> None:
    width = max(len(name) for name in scores)
    for name, value in scores.items():
        arrow = "↑" if METRICS[name].higher_is_better else "↓"
        print(f"{name.upper():<{width}}  {value:.4f}  {arrow}")


def _read_lines(path: str) -> List[str]:
    return Path(path).read_text(encoding="utf-8").splitlines()


def _cmd_list(args: argparse.Namespace) -> int:
    if args.json:
        print(
            json.dumps(
                {
                    m.name: {"description": m.description, "higher_is_better": m.higher_is_better}
                    for m in METRICS.values()
                },
                indent=2,
            )
        )
        return 0
    for m in METRICS.values():
        print(f"{m.name:<7} {'↑' if m.higher_is_better else '↓'}  {m.description}")
    return 0


def _cmd_score(args: argparse.Namespace) -> int:
    scores = evaluate_all(args.ref, args.hyp, _metric_list(args.metric))
    if args.json:
        print(json.dumps(scores, indent=2))
    else:
        _print_scores(scores)
    return 0


def _cmd_corpus(args: argparse.Namespace) -> int:
    hypotheses = _read_lines(args.hyp)
    ref_columns = [_read_lines(path) for path in args.ref]
    for path, column in zip(args.ref, ref_columns, strict=True):
        if len(column) != len(hypotheses):
            raise ValueError(f"{path} has {len(column)} lines but {args.hyp} has {len(hypotheses)}.")
    references = [list(refs) for refs in zip(*ref_columns, strict=True)]

    result = evaluate_corpus(references, hypotheses, _metric_list(args.metric))
    if not args.per_sentence:
        result.pop("sentences")
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    if args.per_sentence:
        for index, scores in enumerate(result["sentences"], start=1):
            print(f"# sentence {index}")
            _print_scores(scores)
        print("# corpus (mean)")
    _print_scores(result["corpus"])
    return 0


def _cmd_serve(args: argparse.Namespace) -> int:
    try:
        import uvicorn
    except ImportError:
        print(
            "The API needs extra dependencies: pip install 'evaluation-machine-translation[api]'",
            file=sys.stderr,
        )
        return 1
    uvicorn.run("eval_mt.api:app", host=args.host, port=args.port, reload=args.reload)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eval-mt",
        description="Evaluate machine translation with BLEU, NIST, GLEU, METEOR, WER and chrF.",
    )
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    metric_help = f"metric to compute, repeatable ({', '.join(METRICS)}, all). Default: all"
    choices = [*METRICS, "all"]

    p_list = sub.add_parser("list", help="list available metrics")
    p_list.add_argument("--json", action="store_true", help="print JSON")
    p_list.set_defaults(func=_cmd_list)

    p_score = sub.add_parser("score", help="score a single sentence")
    p_score.add_argument(
        "-r",
        "--ref",
        action="append",
        required=True,
        help="reference translation, repeat for multiple references",
    )
    p_score.add_argument("-H", "--hyp", required=True, help="machine translation (hypothesis)")
    p_score.add_argument("-m", "--metric", action="append", choices=choices, help=metric_help)
    p_score.add_argument("--json", action="store_true", help="print JSON")
    p_score.set_defaults(func=_cmd_score)

    p_corpus = sub.add_parser("corpus", help="score line-aligned files")
    p_corpus.add_argument(
        "-r",
        "--ref",
        action="append",
        required=True,
        help="reference file (one sentence per line), repeatable",
    )
    p_corpus.add_argument("-H", "--hyp", required=True, help="hypothesis file (one sentence per line)")
    p_corpus.add_argument("-m", "--metric", action="append", choices=choices, help=metric_help)
    p_corpus.add_argument("--per-sentence", action="store_true", help="also show sentence scores")
    p_corpus.add_argument("--json", action="store_true", help="print JSON")
    p_corpus.set_defaults(func=_cmd_corpus)

    p_serve = sub.add_parser("serve", help="run the FastAPI server")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.add_argument("--reload", action="store_true", help="auto-reload (development)")
    p_serve.set_defaults(func=_cmd_serve)

    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, OSError, ZeroDivisionError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
