from mcp_server.registry import TASKS
import logging

logger = logging.getLogger(__name__)


def run_task(task_name: str) -> dict:
    logger.info(f"[ORCHESTRATOR] received task: {task_name}")

    # 🔥 FORÇA fallback inteligente
    if task_name not in TASKS:

        # 🔥 AUTO-ROUTING (mata o problema do Continue)
        if "review" in task_name:
            task_name = "analyze_reviews"

        elif "model" in task_name:
            task_name = "get_models"

        elif "sql" in task_name or "database" in task_name:
            task_name = "business_analysis"

        else:
            logger.error(f"[ORCHESTRATOR] unknown task: {task_name}")
            return {
                "status": "error",
                "message": f"Unknown task: {task_name}"
            }

    try:
        result = TASKS[task_name]()

        logger.info(f"[ORCHESTRATOR] success: {task_name}")

        return {
            "status": "success",
            "task": task_name,
            "result": result
        }

    except Exception as e:
        logger.error(f"[ORCHESTRATOR] error: {str(e)}")

        return {
            "status": "error",
            "task": task_name,
            "message": str(e)
        }