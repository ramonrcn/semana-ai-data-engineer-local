from src.runtime.integrations.antigravity.models import ConversationPayload
from src.runtime.integrations.antigravity.transcript import ConversationTranscript
from src.runtime.integrations.antigravity.transcript_loader import TranscriptLoader


class RequestExtractor:

    def extract(
        self,
        conversation: ConversationPayload,
    ) -> ConversationTranscript:

        loader = TranscriptLoader()

        return loader.load(
            conversation.transcript_path,
        )