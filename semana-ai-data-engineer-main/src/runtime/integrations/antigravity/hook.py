
from src.runtime.application import process_result
from src.runtime.integrations.antigravity.error_handler import ErrorHandler
from src.runtime.integrations.antigravity.artifact_writer import ArtifactWriter
from src.runtime.bootstrap import build_process_user_request
from pathlib import Path
from datetime import datetime
from src.runtime.application.request import RuntimeRequest
from .request_reader import RequestReader
from .error_handler import ErrorHandler
from .request_extractor import RequestExtractor
from .exceptions import InvalidRequestError
from src.runtime.application.process_result import (
    ProcessSuccess,
    RuntimeFailure,
)


def main():
   
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

        transcript = RequestExtractor().extract(
            conversation,
        )

        objective = transcript.last_user_request()

        if not objective:
            raise InvalidRequestError(
                "Antigravity request contains no user objective."
            )

        request = RuntimeRequest(
            objective=objective,
        )

        result = (
            build_process_user_request()
            .execute(
                request=request,
            )
        )

        if isinstance(
            result,
            ProcessSuccess,
        ):

            (
                artifacts / "runtime_response.md"
            ).write_text(
                result.response,
                encoding="utf-8",
            )

        elif isinstance(
            result,
            RuntimeFailure,
        ):

            (
                artifacts / "runtime_error.txt"
            ).write_text(
                (
                    f"code={result.code}\n"
                    f"message={result.message}"
                ),
                encoding="utf-8",
            )

        ArtifactWriter().write_transcript_debug(
            transcript,
            artifacts,
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