from typing import Any, Dict, Literal, Optional
from pydantic import BaseModel


class TaskResponse(BaseModel):
    status: Literal["success", "error"]
    task: Optional[str] = None
    result: Optional[Any] = None
    message: Optional[str] = None
    trace_id: str