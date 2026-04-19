from typing import Dict, Any
from mcp_server.tasks.ping import ping
from mcp_server.tasks.models import get_models
from mcp_server.tasks.database import business_analysis
from mcp_server.tasks.reviews import analyze_reviews
from mcp_server.utils.trace import generate_trace_id
from mcp_server.logging_config import get_logger
from mcp_server.contracts import TaskResponse

logger = get_logger(__name__)


TASK_MAP = {
    "ping": ping,
    "get_models": get_models,
    "business_analysis": business_analysis,
    "analyze_reviews": analyze_reviews,
}


def run_task(task_name: str, **kwargs) -> Dict[str, Any]:
    trace_id = generate_trace_id()

    logger.info(
        f"Received task: {task_name}",
        extra={"trace_id": trace_id}
    )

    if task_name not in TASK_MAP:
        logger.warning(
            f"Unknown task: {task_name}",
            extra={"trace_id": trace_id}
        )

        return TaskResponse(
            status="error",
            message=f"Unknown task: {task_name}",
            trace_id=trace_id,
        ).model_dump()

    try:
        logger.info(
            f"Executing task: {task_name}",
            extra={"trace_id": trace_id}
        )

        result = TASK_MAP[task_name](trace_id=trace_id, **kwargs)

        logger.info(
            f"Task completed: {task_name}",
            extra={"trace_id": trace_id}
        )

        return TaskResponse(
            status="success",
            task=task_name,
            result=result,
            trace_id=trace_id,
        ).model_dump()

    except Exception as e:
        logger.error(
            f"Error in task {task_name}: {str(e)}",
            exc_info=True,
            extra={"trace_id": trace_id}
        )

        return TaskResponse(
            status="error",
            task=task_name,
            message=str(e),
            trace_id=trace_id,
        ).model_dump()