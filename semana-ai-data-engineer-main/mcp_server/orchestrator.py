from typing import Any, Dict

from mcp_server.logging_config import get_logger

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
    logger.info(f"[ORCHESTRATOR] Received task: {task_name} | kwargs: {kwargs}")

    if task_name not in TASK_MAP:
        logger.error(f"[ORCHESTRATOR] Unknown task: {task_name}")
        return {
            "status": "error",
            "message": f"Unknown task: {task_name}"
        }

    try:
        result = TASK_MAP[task_name](**kwargs)

        logger.info(f"[ORCHESTRATOR] Task success: {task_name}")

        return {
            "status": "success",
            "task": task_name,
            "result": result
        }

    except Exception as e:
        logger.exception(f"[ORCHESTRATOR] Task failed: {task_name}")

        return {
            "status": "error",
            "task": task_name,
            "message": str(e)
        }