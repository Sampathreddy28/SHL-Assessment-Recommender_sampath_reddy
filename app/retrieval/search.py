from app.retrieval.vector_store import (
    VectorStore
)


class AssessmentSearchEngine:

    def __init__(self):

        self.store = VectorStore()

        self.store.load()

    def search_assessments(
        self,
        query: str,
        top_k: int = 5
    ):

        results = self.store.search(
            query=query,
            top_k=top_k
        )

        return results