"""Refinement engine that improves generated code using review feedback."""
from __future__ import annotations

from .code_gen import CodeGenTool
from .code_reviewer import CodeReviewerTool

class RefinementEngine:
    def __init__(self, api_key: str | None = None):
        self.generator = CodeGenTool(api_key)
        self.reviewer = CodeReviewerTool(api_key)

    def run_refinement_loop(self, initial_code: str, max_attempts: int = 3) -> str:
        """Run repeated review/refinement cycles until the code passes or max attempts is reached."""
        current_code = initial_code

        for attempt in range(1, max_attempts + 1):
            result = self.reviewer.review(current_code)
            if result["passed"]:
                return current_code

            current_code = self.generator.refine_code(current_code, feedback=str(result["feedback"]))

        return current_code
