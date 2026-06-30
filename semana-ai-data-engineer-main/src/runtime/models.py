from src.runtime.knowledge.models import KnowledgeDocument
from dataclasses import dataclass
from pathlib import Path
import re

@dataclass
class Capability:

    id: str

    name: str

    category: str

    description: str

    tools: list[str]

    model: str

    prompt: str

    source_path: Path

    def extract_kb_refs(
    self
    ) -> list[str]:

        pattern = (
            r"\.claude/kb/([^\s]+)\.md"
        )

        matches = re.findall(
            pattern,
            self.prompt
        )

        refs = []

        for match in matches:

            ref = (
                match
                .replace("/", ".")
                .replace("\\", ".")
            )

            refs.append(ref)

        return sorted(
            set(refs)
        )

    def required_knowledge(self):
        print("\n=== REQUIRED KNOWLEDGE ===")
        print(self.extract_kb_refs())
        return self.extract_kb_refs()
    
    def required_environment_tools(self):
        return self.tools