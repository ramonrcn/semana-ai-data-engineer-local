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

        system_prompt = (
            self.runtime
            .assemble_prompt(
                capability_id,
                objective=""
            )
        )

        return AgentConfig(
            capability_id=capability_id,
            system_instructions=system_prompt
        )