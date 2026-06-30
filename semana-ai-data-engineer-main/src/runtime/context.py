from dataclasses import dataclass

from .models import Capability
from .knowledge.models import KnowledgeDocument


@dataclass
class RuntimeContext:

    capability: Capability

    knowledge: list[KnowledgeDocument]

    environment_tools: list[str]