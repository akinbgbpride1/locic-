import logging
from src.tools.code_gen import CodeGenTool
from src.tools.code_reviewer import CodeReviewerTool
from src.core.refinement import RefinementEngine
from src.core.workflow import ensure_workspace, sanitize_branch_name, execute_command, write_code

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("Orchestrator")

class WorkflowOrchestrator:
    def __init__(self, api_key):
        self.generator = CodeGenTool(api_key)
        self.reviewer = CodeReviewerTool(api_key)
        self.refiner = RefinementEngine(api_key)
        self.workspace = "workshop_dir"

    def run_workflow(self, task_description):
        logger.info(f"Starting workflow: {task_description}")
        ensure_workspace(self.workspace)

        branch_name = sanitize_branch_name(task_description)
        execute_command(["git", "checkout", "-b", branch_name])

        logger.info("Generating code...")
        code = self.generator.generate(task_description)

        logger.info("Reviewing code...")
        review = self.reviewer.review(code)

        if review["passed"]:
            logger.info("Review passed. Writing code and merging branch.")
            write_code(f"{self.workspace}/main.py", code)
            execute_command(["git", "add", "."])
            execute_command(["git", "commit", "-m", f"Implemented {task_description}"])
            execute_command(["git", "checkout", "main"])
            execute_command(["git", "merge", branch_name])
        else:
            logger.warning("Review failed. Code not merged.")
            logger.warning(f"Feedback: {review['feedback']}")
