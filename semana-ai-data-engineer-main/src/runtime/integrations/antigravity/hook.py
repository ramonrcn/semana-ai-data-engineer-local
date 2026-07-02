from pathlib import Path
import json
import sys
import traceback

from .parser import parse_payload


def main():

    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)

    Path("artifacts/python_started.txt").write_text(
        "Python iniciou.",
        encoding="utf-8",
    )

    try:

        # payload = json.loads(
        #     sys.stdin.read()
        # )

        raw = sys.stdin.read()

        (
            artifacts / "payload_raw.json"
        ).write_text(

            raw,

            encoding="utf-8",

        )

        payload = json.loads(raw)

        conversation = parse_payload(
            payload
        )

        transcript = conversation.load_transcript()

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

        (
            artifacts / "last_user_request.txt"
        ).write_text(

            transcript.last_user_request()
            or "None",

            encoding="utf-8",

        )

        (
            artifacts / "conversation.txt"
        ).write_text(

            conversation.summary(),

            encoding="utf-8",

        )

    except Exception:

        (
            artifacts / "gateway_error.txt"
        ).write_text(

            traceback.format_exc(),

            encoding="utf-8",

        )

    print("{}")


if __name__ == "__main__":
    main()