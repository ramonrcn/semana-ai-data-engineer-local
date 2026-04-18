from mcp_server.registry import TASKS
import time
import logging

logger = logging.getLogger(__name__)


def run_task(task_name: str, content: str = ""):
    start = time.time()

    logger.info("[TRACE] INPUT", extra={"task_name": task_name})

    if task_name not in TASKS:
        logger.error("[ERROR] TASK NOT FOUND", extra={"task_name": task_name})
        return {
            "status": "error",
            "message": f"Task {task_name} not found"
        }

    try:
        result = TASKS[task_name]()
        duration = round(time.time() - start, 3)

        logger.info(
            "[TRACE] TASK EXECUTED",
            extra={"task_name": task_name, "duration": duration}
        )

        return {
            "status": "success",
            "task": task_name,
            "duration": duration,
            "result": result,
        }

    except Exception as e:
        logger.error(
            "[ERROR] TASK FAILED",
            extra={"task_name": task_name, "error": str(e)}
        )
        return {
            "status": "error",
            "message": str(e),
        }