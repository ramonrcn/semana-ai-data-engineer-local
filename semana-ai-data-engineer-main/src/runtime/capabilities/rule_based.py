from .detector import BaseCapabilityDetector


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

        raise NotImplementedError(
            f"No capability found for objective: {objective}"
        )