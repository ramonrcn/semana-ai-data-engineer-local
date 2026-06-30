from re import findall

from .selector import BaseKnowledgeSelector


class KeywordKnowledgeSelector(BaseKnowledgeSelector):

    STOPWORDS = {
        "a",
        "an",
        "and",
        "are",
        "be",
        "by",
        "create",
        "for",
        "from",
        "in",
        "is",
        "of",
        "on",
        "the",
        "to",
        "with",
    }

    def select(
        self,
        documents,
        objective: str = "",
    ):

        # Tokenize the objective into normalized keywords.
        keywords = {
            keyword
            for keyword in findall(
                r"\b\w+\b",
                objective.lower(),
            )
            if keyword not in self.STOPWORDS
        }

        ranked_documents = []

        for document in documents:

            # Tokenize the document content.
            content_tokens = set(
                findall(
                    r"\b\w+\b",
                    document.content.lower(),
                )
            )

            # Identify matched keywords for diagnostics.
            matched = [
                keyword
                for keyword in keywords
                if keyword in content_tokens
            ]

            # Score equals the number of matched keywords.
            score = len(matched)

            ranked_documents.append(
                (document, score, matched)
            )

        print("\n=== KEYWORD SCORES ===")

        for document, score, matched in ranked_documents:

            print(
                f"{score:>2} | {document.id} | {matched}"
            )

        # Highest score first.
        ranked_documents.sort(
            key=lambda item: item[1],
            reverse=True,
        )

        return [
            document
            for document, _, _ in ranked_documents
        ]