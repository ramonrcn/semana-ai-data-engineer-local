from src.runtime.application.process_result import (
    ProcessSuccess,
    RuntimeFailure,
)
from src.runtime.application.process_user_request import ProcessUserRequest
from src.runtime.application.request import RuntimeRequest
from src.runtime.exceptions import CapabilityNotFoundError


class SuccessfulDetector:

    def detect(
        self,
        objective: str,
    ) -> str:

        return "test.capability"


class FailingDetector:

    def detect(
        self,
        objective: str,
    ) -> str:

        raise CapabilityNotFoundError(
            f"No capability found for objective: {objective}"
        )


class SuccessfulRuntime:

    def run(
        self,
        capability_id: str,
        objective: str,
    ) -> str:

        return "runtime-success"


class RuntimeThatMustNotExecute:

    def __init__(self):
        self.called = False

    def run(
        self,
        capability_id: str,
        objective: str,
    ) -> str:

        self.called = True

        raise AssertionError(
            "Runtime must not execute after detector failure."
        )


def test_valid_request_returns_process_success():

    process = ProcessUserRequest(
        runtime=SuccessfulRuntime(),
        detector=SuccessfulDetector(),
    )

    request = RuntimeRequest(
        objective="Create Pydantic models"
    )

    result = process.execute(
        request=request
    )

    assert isinstance(
        result,
        ProcessSuccess,
    )

    assert result.response == "runtime-success"


def test_capability_not_found_returns_runtime_failure():

    process = ProcessUserRequest(
        runtime=RuntimeThatMustNotExecute(),
        detector=FailingDetector(),
    )

    request = RuntimeRequest(
        objective="Unsupported objective"
    )

    result = process.execute(
        request=request
    )

    assert isinstance(
        result,
        RuntimeFailure,
    )

    assert (
        result.code
        == "capability_not_found"
    )


def test_runtime_failure_is_never_process_success():

    process = ProcessUserRequest(
        runtime=RuntimeThatMustNotExecute(),
        detector=FailingDetector(),
    )

    request = RuntimeRequest(
        objective="Unsupported objective"
    )

    result = process.execute(
        request=request
    )

    assert isinstance(
        result,
        RuntimeFailure,
    )

    assert not isinstance(
        result,
        ProcessSuccess,
    )


def test_process_success_is_never_runtime_failure():

    process = ProcessUserRequest(
        runtime=SuccessfulRuntime(),
        detector=SuccessfulDetector(),
    )

    request = RuntimeRequest(
        objective="Create Pydantic models"
    )

    result = process.execute(
        request=request
    )

    assert isinstance(
        result,
        ProcessSuccess,
    )

    assert not isinstance(
        result,
        RuntimeFailure,
    )


def test_runtime_failure_preserves_original_error_message():

    objective = "Unsupported objective"

    process = ProcessUserRequest(
        runtime=RuntimeThatMustNotExecute(),
        detector=FailingDetector(),
    )

    request = RuntimeRequest(
        objective=objective
    )

    result = process.execute(
        request=request
    )

    assert isinstance(
        result,
        RuntimeFailure,
    )

    assert result.message == (
        "No capability found for objective: "
        f"{objective}"
    )


def test_pipeline_stops_after_capability_failure():

    runtime = RuntimeThatMustNotExecute()

    process = ProcessUserRequest(
        runtime=runtime,
        detector=FailingDetector(),
    )

    request = RuntimeRequest(
        objective="Unsupported objective"
    )

    result = process.execute(
        request=request
    )

    assert isinstance(
        result,
        RuntimeFailure,
    )

    assert runtime.called is False