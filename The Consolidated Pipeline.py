import subprocess
import logging
import os
from src.tools.code_gen import CodeGenTool
from src.tools.code_reviewer import CodeReviewerTool
from src.core.refinement import RefinementEngine
from src.core.workflow import ensure_workspace, sanitize_branch_name, execute_command, write_code

# Logger setup as defined previously
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger("Orchestrator")

class WorkflowOrchestrator:
    def __init__(self, api_key: str):
        self.generator = CodeGenTool(api_key)
        self.reviewer = CodeReviewerTool(api_key)
        # The Orchestrator now owns the Refinement Engine
        self.refiner = RefinementEngine(api_key) 
        self.workspace = "workshop_dir"

    def run_workflow(self, task_description: str):
        logger.info(f"--- Starting Workflow: {task_description} ---")
        
        try:
            # 1. Setup Environment
            ensure_workspace(self.workspace)
            
            # 2. Start Git Branch
            branch_name = sanitize_branch_name(task_description)
            execute_command(["git", "checkout", "-b", branch_name])
            
            # 3. Initial Generation
            logger.info("Generating initial code draft...")
            initial_code = self.generator.generate(task_description)
            
            # 4. Refinement Loop (The "Self-Healing" Phase)
            logger.info("Entering Refinement Loop...")
            final_code = self.refiner.run_refinement_loop(initial_code, max_attempts=3)
            
            # 5. Final Commit
            write_code(f"{self.workspace}/main.py", final_code)
            execute_command(["git", "add", "."])
            execute_command(["git", "commit", "-m", f"Implemented: {task_description}"])
            execute_command(["git", "checkout", "main"])
            execute_command(["git", "merge", branch_name])
            
            logger.info("Workflow completed successfully.")
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            # Potentially add logic to checkout main and delete branch on failure