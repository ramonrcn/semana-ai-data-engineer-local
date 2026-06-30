from pathlib import Path

from .registry import (
    KnowledgeRegistry
)

registry = (
    KnowledgeRegistry()
)

registry.load_directory(
    Path(".claude/kb")
)

print()

print(
    len(
        registry.list_documents()
    )
)

print()

results = registry.search(
    "shadowtraffic"
)

for result in results:

    print(result.id)