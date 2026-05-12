from pathlib import Path

from prompt_rubric_drift.cli import main
from prompt_rubric_drift.rubric_diff import compare_rubrics


def test_rubric_diff_finds_weights_and_criteria():
    findings = compare_rubrics(Path("examples/before"), Path("examples/after"))
    categories = {item["category"] for item in findings}
    assert "weight_change" in categories
    assert "criteria_removed" in categories
    assert "criteria_added" in categories


def test_cli_compare_generates_report(tmp_path):
    out = tmp_path / "report.md"
    assert main(["compare", "examples/before", "examples/after", "--out", str(out)]) == 0
    text = out.read_text(encoding="utf-8")
    assert "Prompt And Rubric Drift Report" in text
    assert "Suggested Review Questions" in text

