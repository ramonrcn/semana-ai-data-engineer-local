from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeRequest:

    objective: str