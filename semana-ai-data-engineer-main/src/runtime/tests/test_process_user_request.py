from src.runtime.application.process_user_request import ProcessUserRequest
from src.runtime.application.process_result import (
    ProcessSuccess,
    RuntimeFailure,
)
from src.runtime.application.request import RuntimeRequest
from src.runtime.bootstrap import build_runtime
from src.runtime.capabilities.rule_based import RuleBasedCapabilityDetector


process = ProcessUserRequest(
    runtime=build_runtime(),
    detector=RuleBasedCapabilityDetector(),
)


success_request = RuntimeRequest(
    objective="Create Pydantic models"
)

success_result = process.execute(
    request=success_request,
)

assert isinstance(
    success_result,
    ProcessSuccess,
)

assert success_result.response

print(
    "SUCCESS:",
    success_result,
)


failure_request = RuntimeRequest(
    objective="Unsupported objective"
)

failure_result = process.execute(
    request=failure_request,
)

assert isinstance(
    failure_result,
    RuntimeFailure,
)

assert (
    failure_result.code
    == "capability_not_found"
)

assert failure_result.message

print(
    "FAILURE:",
    failure_result,
)