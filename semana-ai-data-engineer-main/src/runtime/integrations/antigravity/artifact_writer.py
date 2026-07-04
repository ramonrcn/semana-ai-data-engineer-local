import json
from pathlib import Path
from .transcript import ConversationTranscript


class ArtifactWriter:
    def write_transcript_debug(
        self,
        transcript: ConversationTranscript,
        artifacts: Path,
    ):
        debug = []

        for event in transcript.events:

            debug.append(

                {

                    "type": event.type,

                    "source": event.source,

                    "status": event.status,

                    "content": event.content,

                }

            )

        (
            artifacts / "transcript_debug.json"
        ).write_text(

            json.dumps(

                debug,

                indent=2,

                ensure_ascii=False,

            ),

            encoding="utf-8",

        )