from pathlib import Path

from .models import KnowledgeDocument


def load_document(
    file_path: Path
) -> KnowledgeDocument:

    content = file_path.read_text(
        encoding="utf-8"
    )

    relative_parts = file_path.parts

    try:
        kb_index = relative_parts.index("kb")
        kb_parts = relative_parts[kb_index + 1 :]
    except ValueError:
        kb_parts = relative_parts

    document_id = ".".join(
        Path(*kb_parts).with_suffix("").parts
    )

    title = file_path.stem

    return KnowledgeDocument(
        id=document_id,
        title=title,
        content=content,
        source_path=file_path
    )