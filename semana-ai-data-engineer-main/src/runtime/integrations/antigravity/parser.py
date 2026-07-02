from pathlib import Path

from .models import ConversationPayload


def parse_payload(
    payload: dict,
) -> ConversationPayload:

    return ConversationPayload(

        conversation_id=payload["conversationId"],

        transcript_path=Path(
            payload["transcriptPath"]
        ),

        artifact_directory=Path(
            payload["artifactDirectoryPath"]
        ),

        workspace_paths=[
            Path(path)
            for path in payload["workspacePaths"]
        ],

        invocation_number=payload["invocationNum"],

        initial_steps=payload["initialNumSteps"],

    )