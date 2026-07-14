from dataclasses import dataclass

from src.runtime.integrations.antigravity.models import ConversationPayload
from src.runtime.conversation.transcript import ConversationTranscript


@dataclass
class ProcessResult:

    response: str

    conversation: ConversationPayload

    transcript: ConversationTranscript