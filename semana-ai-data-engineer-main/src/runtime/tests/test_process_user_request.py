from src.runtime.application.process_user_request import ProcessUserRequest
from src.runtime.bootstrap import build_runtime
from src.runtime.capabilities.rule_based import RuleBasedCapabilityDetector
from src.runtime.integrations.antigravity.models import ConversationPayload

from pathlib import Path


conversation = ConversationPayload(

    conversation_id="test",

    transcript_path=Path("artifacts/transcript.jsonl"),

    artifact_directory=Path("artifacts"),

    workspace_paths=[],

    invocation_number=0,

    initial_steps=0,

)


process = ProcessUserRequest(

    runtime=build_runtime(),

    detector=RuleBasedCapabilityDetector(),

)


result = process.execute(
    conversation,
)


print(result)