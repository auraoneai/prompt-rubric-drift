# prompt-rubric-drift

`prompt-rubric-drift` compares prompt and rubric files across two directories and
generates deterministic PR-review notes. It flags changed scoring boundaries,
criteria additions/deletions, weight changes, stricter or looser wording,
missing examples, prompt-injection exposure, and judge contract drift.

No model call is required.

## Scope

This is not a model judge, policy approval, compliance review, or guarantee that
a prompt or rubric change is safe. It is a deterministic PR-review aid for
surfacing likely drift that still needs human review.

## Quick start

```bash
python -m pip install -e .
prompt-rubric-drift compare examples/before examples/after --out report.md
```

The report is designed to be pasted as a PR comment or published by the bundled
GitHub Action.

## GitHub Action

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: auraoneai/prompt-rubric-drift@v0.1.0
    with:
      before: prompts/base
      after: prompts/head
      output: prompt-rubric-drift.md
      comment: "true"
```

When `comment` is enabled on a pull request event, the action writes the report
to the job summary and creates or updates one deterministic PR comment. Grant
`issues: write` or `pull-requests: write` permission in the workflow.
