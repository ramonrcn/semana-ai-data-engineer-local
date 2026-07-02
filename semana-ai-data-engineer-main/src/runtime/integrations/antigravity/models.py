from anthropic.resources import messages
from dataclasses import dataclass
from pathlib import Path
import json
import time
from .event import ConversationEvent
from .transcript import ConversationTranscript


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
    
    def load_transcript(
        self,
    ) -> ConversationTranscript:

        events = []

        for _ in range(20):

            if self.transcript_path.exists():
                break

            time.sleep(0.1)

        else:

            raise FileNotFoundError(
                self.transcript_path
            )

        with self.transcript_path.open(
            encoding="utf-8",
        ) as file:

            for line in file:

                event = json.loads(
                    line
                )

                events.append(

                    ConversationEvent(

                        source=event["source"],

                        type=event["type"],

                        status=event["status"],

                        created_at=event["created_at"],

                        content=event.get("content"),

                    )

                )

        return ConversationTranscript(
            events=events
        )