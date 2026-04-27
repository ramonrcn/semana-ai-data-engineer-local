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

# --- ALIAS NORMALIZER ---
TASK_ALIASES = {
    "models": "get_models",
    "database": "business_analysis",
    "reviews": "analyze_reviews",
}


def normalize_task(task_name: str, kwargs: dict) -> tuple[str, dict]:

    # --- SAFETY: ensure kwargs is always a dict ---
    if kwargs is None:
        kwargs = {}

    # ✅ FIX 1: protect against non-dict garbage (Continue sometimes sends weird stuff)
    if not isinstance(kwargs, dict):
        kwargs = {"intent": str(kwargs)}

    # --- CLEAN INPUT FROM CONTINUE ---
    if "kwargs" in kwargs:
        raw = kwargs.pop("kwargs")

        if isinstance(raw, str):
            kwargs["intent"] = raw.lower()
        elif isinstance(raw, dict):
            kwargs.update(raw)

    # --- SAFETY: normalize intent ---
    intent = kwargs.get("intent") or ""
    intent = str(intent).lower()  # ✅ FIX 2: ensure always string

    # --- INTENT CLASSIFICATION ---
    if task_name == "business_analysis":

        if any(k in intent for k in [
            "metrics",
            "average_order_value",
            "top_3_states",
            "revenue",
            "distribution",
            "percentage",
            "summary",
            "executive",
        ]):
            kwargs["mode"] = "executive"

        elif any(k in intent for k in [
            "select",
            "query",
            "from",
            "group by",
            "limit",
        ]):
            kwargs["mode"] = "exploration"

        else:
            kwargs["mode"] = "exploration"

    return task_name, kwargs


def run_task(task_name: str, **kwargs) -> Dict[str, Any]:
    trace_id = generate_trace_id()

    logger.info(
        f"Received task: {task_name}",
        extra={"trace_id": trace_id}
    )

    logger.info(f"[DEBUG] FINAL KWARGS: {kwargs}", extra={"trace_id": trace_id})

    # --- STEP 0: HARD NORMALIZATION (CRITICAL ENTRY FIX) ---
    # ✅ FIX 3: normalize full kwargs if someone passes string directly
    if isinstance(kwargs, str):
        kwargs = {"intent": kwargs}

    # existing fix (keep)
    if isinstance(kwargs.get("kwargs"), str):
        kwargs["intent"] = kwargs.pop("kwargs")

    # --- STEP 1: ALIAS NORMALIZATION ---
    normalized_task = TASK_ALIASES.get(task_name, task_name)

    if normalized_task != task_name:
        logger.info(
            f"Alias normalized: {task_name} → {normalized_task}",
            extra={"trace_id": trace_id}
        )

    # --- STEP 2: VALIDATION ---
    if normalized_task not in TASK_MAP:
        logger.warning(
            f"Unknown task: {normalized_task}",
            extra={"trace_id": trace_id}
        )

        return TaskResponse(
            status="error",
            task=normalized_task,  # ✅ FIX 4: always include task
            message=f"Unknown task: {normalized_task}",
            trace_id=trace_id,
        ).model_dump()

    try:
        # --- STEP 3: PARAM NORMALIZATION ---
        kwargs["trace_id"] = trace_id

        normalized_task, kwargs = normalize_task(normalized_task, kwargs)

        logger.info(
            f"Executing task: {normalized_task} with kwargs={kwargs}",
            extra={"trace_id": trace_id}
        )

        # --- STEP 4: EXECUTION ---
        result = TASK_MAP[normalized_task](**kwargs)

        # ✅ FIX 5: NEVER allow None result (this caused your crash)
        if result is None:
            raise ValueError(f"Task {normalized_task} returned None")

        logger.info(
            f"Task completed: {normalized_task}",
            extra={"trace_id": trace_id}
        )

        return TaskResponse(
            status="success",
            task=normalized_task,
            result=result,
            trace_id=trace_id,
        ).model_dump()

    except Exception as e:
        logger.error(
            f"Error in task {normalized_task}: {str(e)}",
            exc_info=True,
            extra={"trace_id": trace_id}
        )

        return TaskResponse(
            status="error",
            task=normalized_task,
            message=str(e),
            trace_id=trace_id,
        ).model_dump()