import subprocess
import os
import logging
from src.tools.code_gen import CodeGenTool
from src.tools.code_reviewer import CodeReviewerTool
from src.tools.refinement_engine import RefinementEngine

# Setup logging for auditability
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("Orchestrator")

class WorkflowOrchestrator:
    def __init__(self, api_key: str):
        self.generator = CodeGenTool(api_key)
        self.refiner = RefinementEngine(api_key)
        self.workspace = "workshop_dir"

    def _execute(self, command: list):
        """Executes a shell command safely."""
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {' '.join(command)}. Error: {e.stderr}")
            raise

    def run_workflow(self, task_description: str):
        logger.info(f"Starting workflow: {task_description}")
        
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)
        
        branch_name = f"feature/{task_description.replace(' ', '_')}"
        
        try:
            # Git operations with error handling
            self._execute(["git", "checkout", "-b", branch_name])
            
            # Integrated Pipeline: Generate -> Refine -> Commit
            code = self.generator.generate(task_description)
            refined_code = self.refiner.run_refinement_loop(code)
            
            # Save and Merge
            with open(f"{self.workspace}/main.py", "w") as f:
                f.write(refined_code)
            
            self._execute(["git", "add", "."])
            self._execute(["git", "commit", "-m", f"Implemented {task_description}"])
            self._execute(["git", "checkout", "main"])
            self._execute(["git", "merge", branch_name])
            
            logger.info("Workflow success.")
            
        except Exception as e:
            logger.critical(f"Pipeline crashed: {e}")