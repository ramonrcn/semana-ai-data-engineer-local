from pathlib import Path
import json
import time

from src.runtime.conversation.transcript import (
    ConversationTranscript,
)
from src.runtime.conversation.event import (
    ConversationEvent,
)


class TranscriptLoader:

    def load(
        self,
        transcript_path: Path,
    ) -> ConversationTranscript:

        events = []

        for _ in range(20):

            if transcript_path.exists():
                break

            time.sleep(0.1)

        else:

            parent = transcript_path.parent

            debug = [
                f"Transcript path: {transcript_path}",
                f"Transcript exists: {transcript_path.exists()}",
                f"Parent path: {parent}",
                f"Parent exists: {parent.exists()}",
            ]

            if parent.exists():
                debug.append("")
                debug.append("Parent contents:")

                for item in sorted(parent.iterdir()):
                    debug.append(f" - {item.name}")

            Path("artifacts/transcript_loader_debug.txt").write_text(
                "\n".join(debug),
                encoding="utf-8",
            )

            raise FileNotFoundError(transcript_path)

        with transcript_path.open(
            encoding="utf-8",
        ) as file:

            for line in file:

                event = json.loads(line)

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