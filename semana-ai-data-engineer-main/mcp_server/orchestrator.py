from mcp_server.registry import TASKS
import time
import logging

logger = logging.getLogger(__name__)


def resolve_task(task_name: str, content: str = ""):
    """
    Resolve the task based on name and content.
    Returns a routing dict with type and value.
    """

    name = task_name.lower()
    content_lower = content.lower()

    # -------------------------
    # 1. Direct task (deterministic)
    # -------------------------
    if name in TASKS:
        return {"type": "task", "value": name}

    # -------------------------
    # 2. Models task (forced routing)
    # -------------------------
    if any(k in content_lower for k in ["pydantic", "basemodel", "models.py", "entities"]):
        return {"type": "task", "value": "get_models"}

    # -------------------------
    # 3. REVIEWS TASK (forced)
    # -------------------------
    if any(k in content_lower for k in ["reviews", "sentiment", "ratings"]):
        return {"type": "task", "value": "analyze_reviews"}

    # -------------------------
    # 5. SQL workflow (LLM-guided)
    # -------------------------
    if any(k in content_lower for k in ["select", "orders", "customers"]):
        return {"type": "workflow", "value": "sql"}

    # -------------------------
    # 5. Fallback
    # -------------------------
    return {"type": "unknown", "value": None}


def run_task(task_name: str, content: str = ""):
    """
    Main execution entrypoint.
    Routes and executes tasks or workflows.
    """

    start = time.time()

    logger.info("[TRACE] INPUT", extra={"task_name": task_name, "step": "start"})

    route = resolve_task(task_name, content)

    logger.info(
        "[TRACE] ROUTE",
        extra={
            "task_name": task_name,
            "step": "resolve",
            "route_type": route.get("type"),
            "route_value": route.get("value"),
        },
    )

    # -------------------------
    # Direct task execution
    # -------------------------
    if route["type"] == "task":
        try:
            result = TASKS[route["value"]]()
            duration = round(time.time() - start, 3)

            logger.info(
                "[TRACE] TASK executed",
                extra={
                    "task_name": route["value"],
                    "step": "execute",
                    "duration": duration,
                },
            )

            return {
                "status": "success",
                "task": route["value"],
                "duration": duration,
                "result": result,
            }

        except Exception as e:
            logger.error(
                "[ERROR] TASK failed",
                extra={
                    "task_name": route.get("value"),
                    "step": "execute",
                    "error": str(e),
                },
            )
            return {
                "status": "error",
                "message": str(e),
            }

    # -------------------------
    # SQL workflow (delegated to agent)
    # -------------------------
    if route["type"] == "workflow":
        logger.info(
            "[TRACE] SQL WORKFLOW triggered",
            extra={"task_name": task_name, "step": "workflow"},
        )

        return {
            "status": "requires_sql_workflow",
            "message": "Use get_schema first, validate SQL, then run_sql",
        }

    # -------------------------
    # Unknown route
    # -------------------------
    logger.warning(
        "[TRACE] UNKNOWN ROUTE",
        extra={"task_name": task_name, "step": "resolve"},
    )

    return {
        "status": "error",
        "message": "Unknown task",
    }