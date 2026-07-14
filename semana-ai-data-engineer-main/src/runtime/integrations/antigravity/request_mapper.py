from src.runtime.integrations.base.models import (
    IntegrationRequest,
)
from src.runtime.integrations.base.request_mapper import (
    BaseRequestMapper,
)
from src.runtime.integrations.antigravity.transcript import (
    ConversationTranscript,
)


class AntigravityRequestMapper(
    BaseRequestMapper,
):

    def map(
        self,
        source: ConversationTranscript,
    ) -> IntegrationRequest:

        return IntegrationRequest(
            message=(
                source.last_user_request()
                or ""
            ),
        )