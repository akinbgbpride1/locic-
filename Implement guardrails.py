import yaml

class WorkflowOrchestrator:
    def __init__(self, api_key):
        with open("config.yaml", "r") as f:
            self.config = yaml.safe_load(f)
        # ...
        
    def run_workflow(self, task):
        # Apply constraint
        if self.config['agent_settings']['auto_merge'] == False:
            logger.info("Auto-merge disabled. Holding for manual approval.")
            # ... add logic to pause execution ...