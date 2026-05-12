from __future__ import annotations


def render_markdown(findings: list[dict[str, str]]) -> str:
    lines = ["# Prompt And Rubric Drift Report", "", f"- Findings: `{len(findings)}`", "", "## PR Review Notes", ""]
    if not findings:
        lines.append("- No deterministic drift findings.")
    for item in findings:
        lines.append(f"- `{item['severity']}` `{item['category']}` `{item['path']}`: {item['message']}")
    lines.extend([
        "",
        "## Suggested Review Questions",
        "",
        "- Did scoring boundaries, criteria, or weights change intentionally?",
        "- Do changed prompts still preserve instruction priority and tool contracts?",
        "- Were examples removed or made inconsistent with the judge contract?",
        "",
    ])
    return "\n".join(lines)

