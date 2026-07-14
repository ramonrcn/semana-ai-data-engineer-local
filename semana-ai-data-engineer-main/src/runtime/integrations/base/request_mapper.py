from abc import ABC, abstractmethod

from .models import IntegrationRequest


class BaseRequestMapper(ABC):

    @abstractmethod
    def map(
        self,
        source,
    ) -> IntegrationRequest:
        ...