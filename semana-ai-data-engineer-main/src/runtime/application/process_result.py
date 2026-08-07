from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProcessSuccess:

    response: str


@dataclass(frozen=True, slots=True)
class RuntimeFailure:

    code: str

    message: str