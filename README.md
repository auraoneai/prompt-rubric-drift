# prompt-rubric-drift

`prompt-rubric-drift` compares prompt and rubric files across two directories and
generates deterministic PR-review notes. It flags changed scoring boundaries,
criteria additions/deletions, weight changes, stricter or looser wording,
missing examples, prompt-injection exposure, and judge contract drift.

No model call is required.

## Quick start

```bash
python -m pip install -e .
prompt-rubric-drift compare examples/before examples/after --out report.md
```

The report is designed to be pasted as a PR comment or published by the bundled
GitHub Action.

