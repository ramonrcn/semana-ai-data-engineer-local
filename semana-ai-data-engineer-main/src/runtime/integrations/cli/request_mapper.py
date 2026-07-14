from src.runtime.integrations.base.models import IntegrationRequest
from src.runtime.integrations.base.request_mapper import BaseRequestMapper


class CLIRequestMapper(
    BaseRequestMapper,
):

    def map(
        self,
        source: str,
    ) -> IntegrationRequest:

        return IntegrationRequest(
            message=source,
        )