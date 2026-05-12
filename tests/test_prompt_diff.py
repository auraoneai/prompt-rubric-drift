from pathlib import Path

from prompt_rubric_drift.prompt_diff import compare_prompts


def test_prompt_diff_finds_strictness_injection_and_missing_examples():
    findings = compare_prompts(Path("examples/before"), Path("examples/after"))
    categories = {item["category"] for item in findings}
    assert "stricter_wording" in categories
    assert "prompt_injection_exposure" in categories
    assert "missing_examples" in categories

