from mcp_server.logging_config import get_logger

logger = get_logger(__name__)

def ping(trace_id=None, **kwargs):
    logger.info("Ping received", extra={"trace_id": trace_id})
    return "pong"