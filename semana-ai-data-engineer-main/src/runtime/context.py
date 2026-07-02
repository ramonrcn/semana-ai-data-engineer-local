from dataclasses import dataclass

from .models import Capability
from .knowledge.retrieved import RetrievedKnowledge


@dataclass
class RuntimeContext:

    capability: Capability

    objective: str

    knowledge: list[RetrievedKnowledge]

    environment_tools: list[str]