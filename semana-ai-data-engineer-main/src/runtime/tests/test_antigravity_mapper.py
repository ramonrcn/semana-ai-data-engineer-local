from src.runtime.integrations.antigravity.event import (
    ConversationEvent,
)
from src.runtime.integrations.antigravity.request_mapper import (
    AntigravityRequestMapper,
)
from src.runtime.integrations.antigravity.transcript import (
    ConversationTranscript,
)


transcript = ConversationTranscript(

    events=[

        ConversationEvent(

            source="user",

            type="USER_INPUT",

            status="completed",

            created_at="2026-07-14T00:00:00",

            content="""
<USER_REQUEST>
Create Pydantic models
</USER_REQUEST>
""",

        ),

    ],

)


mapper = AntigravityRequestMapper()

request = mapper.map(
    transcript,
)

print(request)