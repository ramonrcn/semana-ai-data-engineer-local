from src.runtime.bootstrap import build_runtime
from src.runtime.integrations.antigravity.models import ConversationPayload
from src.runtime.integrations.antigravity.request_extractor import RequestExtractor
from src.runtime.application.process_result import ProcessResult
from src.runtime.runtime import AgentRuntime


class ProcessUserRequest:

    def __init__(
        self,
        runtime: AgentRuntime,
    ):
        self.runtime = runtime

    def execute(
        self,
        conversation: ConversationPayload,
    ) -> ProcessResult:

        try:

            extractor = RequestExtractor()

            transcript = extractor.extract(
                conversation,
            )

            objective = (
                transcript.last_user_request()
                or ""
            )

        except FileNotFoundError:

            return ProcessResult(
                response="",
                conversation=conversation,
                transcript=None,
            )

        response = self.runtime.run(
            capability_id="domain.shopagent-builder",
            objective=objective,
        )

        return ProcessResult(
            response=response,
            conversation=conversation,
            transcript=transcript,
        )