"""Minimal code reviewer for generated Python code."""
from __future__ import annotations

class CodeReviewerTool:
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    def review(self, code: str) -> dict[str, str | bool]:
        """Review code for basic syntax and placeholder issues."""
        if not code.strip():
            return {"passed": False, "feedback": "Generated code is empty."}

        if "TODO" in code or "pass" in code:
            return {
                "passed": False,
                "feedback": "Code contains TODO or pass placeholders and needs refinement."
            }

        try:
            compile(code, "<generated>", "exec")
        except SyntaxError as exc:
            return {"passed": False, "feedback": f"SyntaxError: {exc.msg} at line {exc.lineno}."}
        except Exception as exc:
            return {"passed": False, "feedback": f"Review failed: {exc}."}

        return {"passed": True, "feedback": "Code is syntactically valid."}
