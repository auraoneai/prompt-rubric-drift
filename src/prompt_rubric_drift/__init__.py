"""Prompt and rubric drift detection."""

__version__ = "0.1.7"

from .prompt_diff import compare_prompts
from .report import render_markdown
from .rubric_diff import compare_rubrics

__all__ = ["__version__", "compare_prompts", "compare_rubrics", "render_markdown"]
