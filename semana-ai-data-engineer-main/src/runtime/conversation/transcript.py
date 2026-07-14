from dataclasses import dataclass
from .event import ConversationEvent
import re

@dataclass
class ConversationTranscript:

    events: list[ConversationEvent]

    def last_user_request(
        self,
    ) -> str | None:

        for event in reversed(
            self.events
        ):

            if event.type != "USER_INPUT":
                continue

            if not event.content:
                continue

            match = re.search(

                r"<USER_REQUEST>\s*(.*?)\s*</USER_REQUEST>",

                event.content,

                re.DOTALL,

            )

            if match:

                return match.group(1).strip()

        return None