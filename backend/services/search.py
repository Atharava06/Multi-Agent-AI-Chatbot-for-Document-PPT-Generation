from duckduckgo_search import DDGS

class WebSearchService:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, query: str, max_results: int = 3):
        try:
            results = list(self.ddgs.text(query, max_results=max_results))
            citations = []
            for r in results:
                citations.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "summary": r.get("body")
                })
            return citations
        except Exception as e:
            return [{"error": str(e)}]

search_service = WebSearchService()
