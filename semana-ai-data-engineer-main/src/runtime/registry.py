from anthropic.types.beta import beta_managed_agents_agent_tool_config_params
from pathlib import Path

from .loader import load_capability
from .models import Capability
from .exceptions import (
    CapabilityNotFoundError, DuplicateCapabilityError
)

class CapabilityRegistry:

    def __init__(self):

        self._capabilities = {}

    def register(
        self,
        capability: Capability
    ):

        if capability.id in self._capabilities:

            raise DuplicateCapabilityError(
                f"Capability '{capability.id}' already registered"
            )

        self._capabilities[
            capability.id
        ] = capability
    
    def get(
        self,
        capability_id: str
    ) -> Capability:

        capability = self._capabilities.get(
            capability_id
        )

        if capability is None:
            raise CapabilityNotFoundError(
                f"Capability '{capability_id}' not found"
            )

        return capability
    
    def list(self):
        return sorted(
            self._capabilities.keys()
        )
    
    def load_directory(
        self,
        root: Path
    ):

        for file_path in root.rglob("*.md"):

            print(
                f"Loading: {file_path}"
            )

            capability = load_capability(
                file_path
            )

            print(
                f"Registered: {capability.name}"
            )

            self.register(
                capability
            )