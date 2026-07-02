from dataclasses import dataclass

from .models import KnowledgeDocument


@dataclass
class RetrievedKnowledge:

    document: KnowledgeDocument

    score: float | None = None

    rank: int | None = None