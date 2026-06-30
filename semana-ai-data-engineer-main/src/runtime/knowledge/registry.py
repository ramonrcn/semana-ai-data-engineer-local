from anthropic.types.beta import beta_refusal_stop_details
from pathlib import Path

from .loader import load_document
from .models import KnowledgeDocument

class KnowledgeRegistry:

    def __init__(self):

        self._documents = {}

    def register(
        self,
        document: KnowledgeDocument
    ):

        self._documents[
            document.id
        ] = document

    def get(
        self,
        document_id: str
    ) -> KnowledgeDocument:

        return self._documents[
            document_id
        ]

    def list_documents(self):

        return sorted(
            self._documents.keys()
        )

    def load_directory(
        self,
        root: Path
    ):

        for file_path in root.rglob(
            "*.md"
        ):

            document = load_document(
                file_path
            )

            self.register(
                document
            )

    def search(
        self,
        query: str
    ) -> list[KnowledgeDocument]:

        query = query.lower()

        matches = []

        for document in self._documents.values():

            if (
                query in document.id.lower()
                or query in document.title.lower()
            ):

                matches.append(
                    document
                )

        return matches
    
    def resolve(self,refs: list[str]) -> list[KnowledgeDocument]:
        documents = []

        for ref in refs:

            try:

                documents.append(
                    self.get(ref)
                )

            except KeyError:

                pass

        return documents