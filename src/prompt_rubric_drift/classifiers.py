from __future__ import annotations

STRICTER = ("must", "required", "never", "always", "only if", "reject")
LOOSER = ("may", "optional", "usually", "try to", "can")
INJECTION = ("ignore previous", "system prompt", "developer message", "tool output", "untrusted")


def classify_text(before: str, after: str, path: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    lower_before = before.lower()
    lower_after = after.lower()
    for phrase in STRICTER:
        if lower_after.count(phrase) > lower_before.count(phrase):
            findings.append({"severity": "medium", "category": "stricter_wording", "path": path, "message": f"increased strictness marker `{phrase}`"})
    for phrase in LOOSER:
        if lower_after.count(phrase) > lower_before.count(phrase):
            findings.append({"severity": "medium", "category": "looser_wording", "path": path, "message": f"increased looseness marker `{phrase}`"})
    for phrase in INJECTION:
        if phrase in lower_after and phrase not in lower_before:
            findings.append({"severity": "high", "category": "prompt_injection_exposure", "path": path, "message": f"new injection-sensitive phrase `{phrase}`"})
    if "example" in lower_before and "example" not in lower_after:
        findings.append({"severity": "medium", "category": "missing_examples", "path": path, "message": "examples removed from prompt or rubric"})
    return findings

