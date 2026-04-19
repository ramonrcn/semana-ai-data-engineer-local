from typing import Dict, Any
from mcp_server.tasks.ping import ping
from mcp_server.tasks.models import get_models
from mcp_server.tasks.database import business_analysis


TASK_MAP = {
    "ping": ping,
    "get_models": get_models,
    "business_analysis": business_analysis
}


def run_task(task_name: str, **kwargs) -> Dict[str, Any]:
    if task_name not in TASK_MAP:
        return {
            "status": "error",
            "message": f"Unknown task: {task_name}"
        }

    try:
        result = TASK_MAP[task_name](**kwargs)

        return {
            "status": "success",
            "task": task_name,
            "result": result
        }

    except Exception as e:
        return {
            "status": "error",
            "task": task_name,
            "message": str(e)
        }