from abc import ABC, abstractmethod


class BaseCapabilityDetector(ABC):

    @abstractmethod
    def detect(
        self,
        objective: str,
    ) -> str:
        ...