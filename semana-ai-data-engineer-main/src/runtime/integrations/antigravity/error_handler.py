from pathlib import Path
import traceback


class ErrorHandler:

    def handle(
        self,
        artifacts: Path,
    ):

        (
            artifacts / "gateway_error.txt"
        ).write_text(

            traceback.format_exc(),

            encoding="utf-8",

        )