from src.runtime.bootstrap import build_runtime
from src.runtime.integrations.antigravity.error_handler import ErrorHandler
from src.runtime.integrations.antigravity.artifact_writer import ArtifactWriter
from src.runtime.application.process_user_request import ProcessUserRequest
from src.runtime.capabilities.rule_based import RuleBasedCapabilityDetector
from pathlib import Path
from datetime import datetime

from .request_reader import RequestReader
from .error_handler import ErrorHandler


def main():
    # WIP - Antigravity testing
    # import json
    # import sys

    # print("STDOUT")

    # print("STDERR", file=sys.stderr)
    # Path(".agents/artifacts/experiment.txt").write_text(
    # "hook executou",
    # encoding="utf-8",
    # )

    # from pathlib import Path
    # from datetime import datetime

    # Path(".agents/artifacts/preinvocation.txt").write_text(
    #     datetime.now().isoformat(),
    #     encoding="utf-8",
    # )

    # print("done")

    artifacts = Path(".agents/artifacts")
    artifacts.mkdir(exist_ok=True)

    (
        artifacts / "python_started.txt"
    ).write_text(
        datetime.now().isoformat(),
        encoding="utf-8",
    )

    try:

        conversation = RequestReader().read()

        result = ProcessUserRequest(
            runtime=build_runtime(),
            detector=RuleBasedCapabilityDetector(),
        ).execute(
            conversation=conversation,
        )

        (
            artifacts / "runtime_response.md"
        ).write_text(
            result.response,
            encoding="utf-8",
        )

        ArtifactWriter().write_transcript_debug(
            result.transcript,
            artifacts,
        )

        (
            artifacts / "last_user_request.txt"
        ).write_text(
            result.transcript.last_user_request()
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

        ErrorHandler().handle(
            artifacts,
        )

    (
        artifacts / "python_finished.txt"
    ).write_text(
        datetime.now().isoformat(),
        encoding="utf-8",
    )

    print("{}")

if __name__ == "__main__":
    main()