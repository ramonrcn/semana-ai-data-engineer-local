from src.runtime.application.request import RuntimeRequest
from src.runtime.application.process_result import (
    ProcessSuccess,
    RuntimeFailure,
)
from src.runtime.runtime import AgentRuntime
from src.runtime.capabilities.detector import BaseCapabilityDetector
from src.runtime.exceptions import CapabilityNotFoundError


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
        request: RuntimeRequest,
    ) -> ProcessSuccess | RuntimeFailure:

        try:

            capability_id = self.detector.detect(
                request.objective,
            )

            response = self.runtime.run(
                capability_id=capability_id,
                objective=request.objective,
            )

            return ProcessSuccess(
                response=response,
            )

        except CapabilityNotFoundError as exc:

            return RuntimeFailure(
                code="capability_not_found",
                message=str(exc),
            )