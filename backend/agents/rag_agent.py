from services.vector_store import vector_store

class RAGAgent:
    def retrieve(self, query: str) -> dict:
        results = vector_store.search(query, k=3)
        return {
            "query": query,
            "results": results
        }
