import argparse
import logging

import yaml
from src.tools.code_gen import CodeGenTool
from src.tools.code_reviewer import CodeReviewerTool
from src.core.refinement import RefinementEngine
from src.core.workflow import ensure_workspace, sanitize_branch_name, execute_command, write_code

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("Guardrails")

class WorkflowOrchestrator:
    def __init__(self, api_key):
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)

        self.generator = CodeGenTool(api_key)
        self.reviewer = CodeReviewerTool(api_key)
        self.refiner = RefinementEngine(api_key)
        self.workspace = "workshop_dir"

    def run_workflow(self, task):
        ensure_workspace(self.workspace)

        if self.config.get("agent_settings", {}).get("auto_merge") is False:
            logger.info("Auto-merge disabled. Holding for manual approval.")
            return

        branch_name = sanitize_branch_name(task)
        execute_command(["git", "checkout", "-b", branch_name])

        logger.info("Generating code...")
        code = self.generator.generate(task)

        logger.info("Reviewing code...")
        review = self.reviewer.review(code)

        if review["passed"]:
            logger.info("Review passed. Writing code and merging branch.")
            write_code(f"{self.workspace}/main.py", code)
            execute_command(["git", "add", "."])
            execute_command(["git", "commit", "-m", f"Implemented {task}"])
            execute_command(["git", "checkout", "main"])
            execute_command(["git", "merge", branch_name])
        else:
            logger.warning("Review failed. Code not merged.")
            logger.warning(f"Feedback: {review['feedback']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the guardrails-enabled workflow orchestrator.")
    parser.add_argument("task", help="Task description for code generation.")
    parser.add_argument("--api-key", help="Optional API key for tooling.")
    args = parser.parse_args()

    orchestrator = WorkflowOrchestrator(api_key=args.api_key)
    orchestrator.run_workflow(args.task)


if __name__ == "__main__":
    main()
