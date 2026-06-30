from dataclasses import dataclass
from pathlib import Path


@dataclass
class KnowledgeDocument:

    id: str

    title: str

    content: str

    source_path: Path