from services.search import search_service
from services.gemini import gemini_service
import json

class ResearchAgent:
    def research(self, query: str) -> dict:
        # Search the web
        results = search_service.search(query, max_results=3)
        
        # Summarize with Gemini
        prompt = f"Summarize the following search results about '{query}':\n\n{json.dumps(results)}"
        summary = gemini_service.generate_text(prompt)
        
        return {
            "query": query,
            "citations": results,
            "summary": summary
        }
