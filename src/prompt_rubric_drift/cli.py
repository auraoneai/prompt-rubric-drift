from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .prompt_diff import compare_prompts
from .report import render_markdown
from .rubric_diff import compare_rubrics


def compare(args: argparse.Namespace) -> int:
    before = Path(args.before)
    after = Path(args.after)
    findings = compare_prompts(before, after) + compare_rubrics(before, after)
    output = render_markdown(findings)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-rubric-drift")
    sub = parser.add_subparsers(dest="command", required=True)
    compare_parser = sub.add_parser("compare")
    compare_parser.add_argument("before")
    compare_parser.add_argument("after")
    compare_parser.add_argument("--out")
    compare_parser.set_defaults(func=compare)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

