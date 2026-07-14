from src.runtime.bootstrap import build_runtime
from src.runtime.integrations.antigravity.models import ConversationPayload
from src.runtime.integrations.antigravity.request_extractor import RequestExtractor
from src.runtime.application.process_result import ProcessResult
from src.runtime.runtime import AgentRuntime
from src.runtime.capabilities.detector import BaseCapabilityDetector

class ProcessUserRequest:

    def __init__(
        self,
        runtime: AgentRuntime,
        detector: BaseCapabilityDetector,
    ):
        self.runtime = runtime
        self.detector = detector

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

            capability_id = self.detector.detect(
                objective,
            )

        except FileNotFoundError:

            return ProcessResult(
                response="",
                conversation=conversation,
                transcript=None,
            )

        response = self.runtime.run(
            capability_id=capability_id,
            objective=objective,
        )

        return ProcessResult(
            response=response,
            conversation=conversation,
            transcript=transcript,
        )