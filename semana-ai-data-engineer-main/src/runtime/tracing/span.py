from .event import TraceEvent
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .trace import RuntimeTrace


class TraceSpan:

    def __init__(
        self,
        event: TraceEvent,
    ):

        self.event = event

    def __enter__(self):

        return self.event

    def __exit__(
        self,
        exc_type,
        exc,
        tb,
    ):

        self.event.finish()