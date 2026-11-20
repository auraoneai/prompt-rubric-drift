# prompt-rubric-drift

**LLM evaluation prompt and rubric drift review** for pull requests, offline and deterministic.

> Part of [Rubric Studio](https://auraone.ai/open/rubric-studio-open). Use it alongside Rubric Studio to get a deterministic first-pass review of prompt and rubric file changes before merge.

## Quick Start

```bash
python -m pip install prompt-rubric-drift==0.1.7
prompt-rubric-drift compare examples/before examples/after --out drift-report.md
```

Compare prompt and rubric directories and produce deterministic pull request review notes.

`prompt-rubric-drift` is for prompt owners, evaluation engineers, and reviewers who need a repeatable first pass over scoring-contract changes. Its differentiator is an offline, deterministic review of both prompt and rubric files, using local text, JSON, and regex heuristics to flag stricter or looser wording, prompt-injection exposure, missing examples, judge-contract terms, weight changes, and added or removed criteria without calling a model.

## Inspectable Output

- Markdown: finding count, severity/category/path rows, and suggested review questions.
- JSON: `ok`, `finding_count`, and the complete structured finding list.
- GitHub Action: the Markdown report file, job summary content, and an optional marker-matched pull request comment.

## Runtime Boundary

The Python CLI reads only the two local directories and makes no network requests or model calls. The composite GitHub Action installs the package from the checked-out action path, writes to `GITHUB_STEP_SUMMARY`, and uses `actions/github-script` to list, create, or update pull request comments when `comment: "true"`.

Prompt scanning covers `.txt`, `.md`, and `.prompt`; rubric scanning covers `.json`, `.yaml`, `.yml`, and `.md`. The comparison walks the `after` tree, so a file deleted entirely from `after` is not reported as a file deletion.

## Install

Python package:

```bash
python -m pip install prompt-rubric-drift==0.1.7
```

GitHub Action:

```yaml
permissions:
  contents: read
  pull-requests: write

steps:
  - uses: actions/checkout@v4
  - uses: auraoneai/prompt-rubric-drift@v0.1.7
    with:
      before: prompts/base
      after: prompts/head
      output: prompt-rubric-drift.md
      comment: "true"
```

Both directories must already exist in the checked-out workspace.

## Quickstart

```bash
prompt-rubric-drift compare examples/before examples/after --out drift-report.md
prompt-rubric-drift compare examples/before examples/after --format json --out drift-report.json
```

## Release Status

Registry status verified July 13, 2026:

- Python package `0.1.7` is published on PyPI.
- The installed CLI supports both Markdown and JSON output.
- The latest public GitHub Action tag is `v0.1.7`.
- No moving `v1` tag or npm package is claimed.

The project is alpha software. No safety, compliance, or adoption claim is made.

## Limits

Findings are deterministic heuristics, not semantic proof. The tool does not approve prompt changes, detect all file deletions, run an LLM judge, or guarantee that a prompt or rubric is safe.

## Next Action

Use the installed CLI or `v0.1.7` Action, then review high-severity findings with the rubric owner before gating pull requests.
