from __future__ import annotations

import json
import re
from pathlib import Path

from .classifiers import classify_text

RUBRIC_EXTENSIONS = {".json", ".yaml", ".yml", ".md"}
WEIGHT_RE = re.compile(r"\"?weight\"?\s*[:=]\s*([0-9.]+)", re.IGNORECASE)


def compare_rubrics(before: Path, after: Path) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    for path in sorted(after.rglob("*")):
        if not path.is_file() or path.suffix not in RUBRIC_EXTENSIONS:
            continue
        rel = path.relative_to(after)
        old = before / rel
        if not old.exists():
            findings.append({"severity": "medium", "category": "new_rubric", "path": str(rel), "message": "new rubric file added"})
            continue
        before_text = old.read_text(encoding="utf-8")
        after_text = path.read_text(encoding="utf-8")
        findings.extend(classify_text(before_text, after_text, str(rel)))
        findings.extend(compare_weights(before_text, after_text, str(rel)))
        findings.extend(compare_criteria(before_text, after_text, str(rel)))
    return findings


def compare_weights(before: str, after: str, path: str) -> list[dict[str, str]]:
    if WEIGHT_RE.findall(before) != WEIGHT_RE.findall(after):
        return [{"severity": "high", "category": "weight_change", "path": path, "message": "rubric weights changed"}]
    return []


def compare_criteria(before: str, after: str, path: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    before_items = extract_criteria(before)
    after_items = extract_criteria(after)
    removed = before_items - after_items
    added = after_items - before_items
    if removed:
        findings.append({"severity": "high", "category": "criteria_removed", "path": path, "message": f"removed criteria: {', '.join(sorted(removed))}"})
    if added:
        findings.append({"severity": "medium", "category": "criteria_added", "path": path, "message": f"added criteria: {', '.join(sorted(added))}"})
    return findings


def extract_criteria(text: str) -> set[str]:
    try:
        data = json.loads(text)
        criteria = data.get("criteria", []) if isinstance(data, dict) else []
        return {str(item.get("name", item)).lower() for item in criteria}
    except json.JSONDecodeError:
        return {line.strip("- *").strip().lower() for line in text.splitlines() if line.strip().lower().startswith(("- criterion:", "* criterion:"))}
