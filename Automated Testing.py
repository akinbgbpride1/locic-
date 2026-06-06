import subprocess
import logging

logger = logging.getLogger("RefinementEngine")

class RefinementEngine:
    # ... existing __init__ ...

    def run_tests(self, test_file="tests/test_main.py"):
        """Runs pytest and returns the output."""
        try:
            result = subprocess.run(
                ["pytest", test_file], 
                capture_output=True, 
                text=True
            )
            if result.returncode == 0:
                return True, "All tests passed."
            return False, result.stdout + result.stderr
        except Exception as e:
            return False, str(e)

    def run_refinement_loop(self, initial_code, max_attempts=3):
        # ... logic to save code to file ...
        for attempt in range(max_attempts):
            success, feedback = self.run_tests()
            if success:
                return current_code
            
            logger.warning(f"Tests failed on attempt {attempt+1}. Refining...")
            current_code = self.generator.refine_code(current_code, feedback)
        return current_code