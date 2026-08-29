from services.gemini import gemini_service

class AnalysisAgent:
    def analyze_style(self, text_content: str, filename: str) -> str:
        if not text_content.strip():
            return "No content to analyze."
        prompt = f"Analyze the following content from '{filename}' and describe its tone, formatting style, and target audience in 2-3 sentences. This will be used as a style guide for generating new content.\n\nContent:\n{text_content[:3000]}"
        return gemini_service.generate_text(prompt)
