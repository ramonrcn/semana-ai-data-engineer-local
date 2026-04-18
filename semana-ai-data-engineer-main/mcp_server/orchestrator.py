from typing import Dict, Any
from mcp_server.logging_config import get_logger

# Tasks
from mcp_server.tasks.models import get_models
from mcp_server.tasks.database import business_analysis
from mcp_server.tasks.reviews import analyze_reviews_task

logger = get_logger(__name__)

TASK_MAP = {
    "get_models": get_models,
    "business_analysis": business_analysis,
    "analyze_reviews": analyze_reviews_task,
}


def run_task(task_name: str, **kwargs) -> Dict[str, Any]:
    logger.info(f"[ORCHESTRATOR] Requested task: {task_name}")

    if task_name not in TASK_MAP:
        logger.error(f"[ORCHESTRATOR] Unknown task: {task_name}")
        return {
            "status": "error",
            "message": f"Unknown task: {task_name}"
        }

    try:
        task_fn = TASK_MAP[task_name]

        logger.info(f"[ORCHESTRATOR] Executing task: {task_name}")
        result = task_fn(**kwargs)

        logger.info(f"[ORCHESTRATOR] Task {task_name} executed successfully")

        return {
            "status": "success",
            "task": task_name,
            "result": result
        }

    except Exception as e:
        logger.exception(f"[ORCHESTRATOR] Error executing task {task_name}")
        return {
            "status": "error",
            "task": task_name,
            "message": str(e)
        }