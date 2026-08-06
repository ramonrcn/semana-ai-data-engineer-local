from dataclasses import dataclass

from ..runtime import AgentRuntime


@dataclass
class AgentConfig:

    capability_id: str

    system_instructions: str


class AgentBuilder:

    def __init__(
        self,
        runtime: AgentRuntime
    ):
        self.runtime = runtime

    def build_config(
        self,
        capability_id: str
    ) -> AgentConfig:

        context = self.runtime.build_context(
            capability_id=capability_id,
            objective=""
        )

        system_prompt = (
            self.runtime
            .assemble_prompt(
                context
            )
        )

        return AgentConfig(
            capability_id=capability_id,
            system_instructions=system_prompt.text
        )