from __future__ import annotations

from pathlib import Path

from .classifiers import classify_text

PROMPT_EXTENSIONS = {".txt", ".md", ".prompt"}


def compare_prompts(before: Path, after: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in sorted(after.rglob("*")):
        if not path.is_file() or path.suffix not in PROMPT_EXTENSIONS:
            continue
        rel = path.relative_to(after)
        old = before / rel
        if not old.exists():
            findings.append({"severity": "medium", "category": "new_prompt", "path": str(rel), "message": "new prompt file added"})
            continue
        findings.extend(classify_text(old.read_text(encoding="utf-8"), path.read_text(encoding="utf-8"), str(rel)))
    return findings

