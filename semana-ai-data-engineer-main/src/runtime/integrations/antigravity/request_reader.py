from pathlib import Path
import json
import sys

from .parser import parse_payload
from .models import ConversationPayload


class RequestReader:

    def read(
        self,
    ) -> ConversationPayload:

        raw = sys.stdin.read()

        Path("artifacts/payload_raw.json").write_text(
            raw,
            encoding="utf-8",
        )

        payload = json.loads(raw)

        return parse_payload(
            payload
        )