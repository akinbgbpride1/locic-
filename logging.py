import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout), # Console output
            logging.FileHandler("agent_workflow.log") # File persistence
        ]
    )
    return logging.getLogger("InvestmentAgent")