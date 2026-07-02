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

        payload = json.loads(
            sys.stdin.read()
        )

        conversation = parse_payload(
            payload
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