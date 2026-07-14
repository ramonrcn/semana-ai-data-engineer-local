from dataclasses import dataclass


@dataclass
class ConversationEvent:

    source: str

    type: str

    status: str

    created_at: str

    content: str | None = None