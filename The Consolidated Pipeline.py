import subprocess
import logging
import os
from src.tools.code_gen import CodeGenTool
from src.tools.code_reviewer import CodeReviewerTool
from src.core.refinement import RefinementEngine # Assuming your refiner is here

# Logger setup as defined previously
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
            if not os.path.exists(self.workspace):
                os.makedirs(self.workspace)
            
            # 2. Start Git Branch
            branch_name = f"feature/{task_description.replace(' ', '_')}"
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
            
            # 3. Initial Generation
            logger.info("Generating initial code draft...")
            initial_code = self.generator.generate(task_description)
            
            # 4. Refinement Loop (The "Self-Healing" Phase)
            logger.info("Entering Refinement Loop...")
            final_code = self.refiner.run_refinement_loop(initial_code, max_attempts=3)
            
            # 5. Final Commit
            with open(f"{self.workspace}/main.py", "w") as f:
                f.write(final_code)
            
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"Implemented: {task_description}"], check=True)
            subprocess.run(["git", "checkout", "main"], check=True)
            subprocess.run(["git", "merge", branch_name], check=True)
            
            logger.info("Workflow completed successfully.")
            
        except Exception as e:
            logger.error(f"Workflow failed: {e}")
            # Potentially add logic to checkout main and delete branch on failure