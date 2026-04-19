from mcp_server.logging_config import get_logger

logger = get_logger("test")

logger.info("Test log without trace")
logger.info("Test log with trace", extra={"trace_id": "abc-123"})