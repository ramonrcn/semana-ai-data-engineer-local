from .selector import BaseKnowledgeSelector
from ..similarity.base import BaseSimilarityMetric
from ..similarity.cosine import CosineSimilarityMetric


class VectorKnowledgeSelector(BaseKnowledgeSelector):

    def __init__(
        self,
        similarity: BaseSimilarityMetric | None = None,
    ) -> None:

        self.similarity = (
            similarity
            or CosineSimilarityMetric()
        )