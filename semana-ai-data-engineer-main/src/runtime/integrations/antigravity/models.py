from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConversationPayload:

    conversation_id: str

    transcript_path: Path

    artifact_directory: Path

    workspace_paths: list[Path]

    invocation_number: int

    initial_steps: int

    def summary(self) -> str:

        return f"""
            Conversation ID : {self.conversation_id}

            Transcript      : {self.transcript_path}

            Artifacts       : {self.artifact_directory}

            Workspace       : {self.workspace_paths}

            Invocation      : {self.invocation_number}

            Initial Steps   : {self.initial_steps}
            """