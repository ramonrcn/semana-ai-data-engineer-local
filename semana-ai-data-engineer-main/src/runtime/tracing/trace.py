from anthropic.types.beta import beta_managed_agents_agent_tool_config_params
from dataclasses import dataclass, field
from time import perf_counter
from uuid import uuid4
from .event import TraceEvent
from .span import TraceSpan


@dataclass
class RuntimeTrace:

    execution_id: str

    started_at: float

    finished_at: float | None = None

    capability: str = ""

    objective: str = ""

    knowledge_selector: str = ""

    knowledge_documents: int = 0

    prompt_size: int = 0

    llm: str = ""

    events: list[TraceEvent] = field(
        default_factory=list
    )

    @classmethod
    def start(cls):

        return cls(

            execution_id=uuid4().hex[:8],

            started_at=perf_counter(),

        )

    def finish(self):

        self.finished_at = perf_counter()

    @property
    def elapsed_ms(self):

        if self.finished_at is None:
            return 0

        return (
            self.finished_at
            - self.started_at
        ) * 1000
    
    @property
    def timeline(self):

        return tuple(
            self.events
        )

    def add_event(
        self,
        name: str,
        **attributes,
    ):

        event = TraceEvent(

            name=name,

            attributes=attributes,

        )

        self.events.append(event)

        return event

    def span(
        self,
        name: str,
        **attributes,
    ):

        event = self.add_event(
            name,
            **attributes,
        )

        return TraceSpan(
            event,
        )
    
    # Backwards compatibility alias
    def event(
        self,
        name: str,
        **attributes,
    ):

        return self.span(
            name,
            **attributes,
        )