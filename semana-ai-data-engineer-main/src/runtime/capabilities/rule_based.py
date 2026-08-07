from .detector import BaseCapabilityDetector
from src.runtime.exceptions import CapabilityNotFoundError


class RuleBasedCapabilityDetector(
    BaseCapabilityDetector,
):

    def detect(
        self,
        objective: str,
    ) -> str:

        objective = objective.lower()

        if "pydantic" in objective:
            return "domain.shopagent-builder"

        raise CapabilityNotFoundError(
            f"No capability found for objective: {objective}"
        )