import subprocess
import os
import shutil
from src.tools.code_gen import CodeGenTool
from src.tools.code_reviewer import CodeReviewerTool

class WorkflowOrchestrator:
    def __init__(self, api_key):
        self.generator = CodeGenTool(api_key)
        self.reviewer = CodeReviewerTool(api_key)
        self.workspace = "workshop_dir"

    def run_workflow(self, task_description):
        # 1. Generate Workshop
        if not os.path.exists(self.workspace):
            os.makedirs(self.workspace)
        
        # 2. Generate Branch
        branch_name = f"feature/{task_description.replace(' ', '_')}"
        subprocess.run(["git", "checkout", "-b", branch_name])
        
        # 3. Generate Python Code
        print("Generating code...")
        code = self.generator.generate(task_description)
        
        # 4. Review Code
        print("Reviewing code...")
        review = self.reviewer.review(code)
        
        # 5. Merge Reviewed Code (Conditional)
        if review["passed"]:
            print("Review Passed! Merging code...")
            with open(f"{self.workspace}/main.py", "w") as f:
                f.write(code)
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", f"Implemented {task_description}")
            subprocess.run(["git", "checkout", "main"])
            subprocess.run(["git", "merge", branch_name])
        else:
            print("Review Failed! Code not merged.")
            print(f"Feedback: {review['feedback']}")
