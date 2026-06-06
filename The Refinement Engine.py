from src.tools.code_gen import CodeGenTool
from src.tools.code_reviewer import CodeReviewerTool

class RefinementEngine:
    def __init__(self, api_key: str):
        self.generator = CodeGenTool(api_key)
        self.reviewer = CodeReviewerTool(api_key)

    def run_refinement_loop(self, initial_code: str, max_attempts=3):
        current_code = initial_code
        
        for attempt in range(max_attempts):
            print(f"--- Attempt {attempt + 1} ---")
            
            # 1. Review the current code
            result = self.reviewer.review(current_code)
            
            # 2. Check for success (Break the loop)
            if result["passed"]:
                print("Code review passed! Breaking loop.")
                return current_code
            
            # 3. If it failed, use feedback to improve the code
            print("Review failed. Refining code...")
            current_code = self.generator.refine_code(
                current_code, 
                feedback=result["feedback"]
            )
            
        print("Max attempts reached. Returning best effort.")
        return current_code