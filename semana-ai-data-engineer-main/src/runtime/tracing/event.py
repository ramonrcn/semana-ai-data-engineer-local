from dataclasses import dataclass, field
from time import perf_counter


@dataclass
class TraceEvent:

    name: str

    started_at: float = field(
        default_factory=perf_counter
    )

    finished_at: float | None = None

    attributes: dict = field(
        default_factory=dict
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
    
    def __setitem__(
        self,
        key,
        value,
    ):

        self.attributes[key] = value
    
    def __getitem__(
        self,
        key,
    ):

        return self.attributes[key]
    
    def add(
        self,
        **attributes,
    ):

        self.attributes.update(
            attributes
        )

        return self