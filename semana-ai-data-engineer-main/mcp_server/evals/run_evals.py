from mcp_server.orchestrator import run_task
import logging

logger = logging.getLogger(__name__)

tests = [
    {
        "name": "models",
        "input": "models",
        "expected_status": "success",
    },
    {
        "name": "sql_workflow",
        "input": "07",
        "content": "orders customers analysis",
        "expected_status": "requires_sql_workflow",
    },
]


def run():
    logger.info("[TEST] Starting evaluation suite")

    for test in tests:
        logger.info("[TEST] Running", extra={"task_name": test["name"], "step": "eval"})

        result = run_task(
            test["input"],
            test.get("content", ""),
        )

        status = result.get("status")

        if status == test["expected_status"]:
            logger.info(
                "[TEST] PASS",
                extra={"task_name": test["name"], "step": "eval"},
            )
        else:
            logger.error(
                "[TEST] FAIL",
                extra={
                    "task_name": test["name"],
                    "step": "eval",
                    "expected": test["expected_status"],
                    "got": status,
                },
            )


if __name__ == "__main__":
    run()