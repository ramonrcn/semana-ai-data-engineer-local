from sklearn.feature_extraction.text import TfidfVectorizer

from .vector import VectorKnowledgeSelector


class TFIDFKnowledgeSelector(VectorKnowledgeSelector):

    def __init__(
        self,
        top_k: int | None = None,
        similarity=None,
    ):

        super().__init__(similarity)

        self._top_k = top_k

    def select(
        self,
        documents,
        objective: str = "",
    ):

        corpus = [
            document.content
            for document in documents
        ]

        vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        tfidf = vectorizer.fit_transform(
            corpus + [objective]
        )

        objective_vector = tfidf[-1]

        document_vectors = tfidf[:-1]

        # Display the effective query terms recognized by TF-IDF.
        print("\n=== TF-IDF QUERY TERMS ===")

        query_terms = sorted(
            set(vectorizer.build_analyzer()(objective))
        )

        print(query_terms)


        return self._rank_documents(
            documents,
            document_vectors,
            objective_vector,
        )