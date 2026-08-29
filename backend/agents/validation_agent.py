from services.parser import parser_service
from services.gemini import gemini_service

class ValidationAgent:
    def validate(self, filename: str) -> dict:
        source_path = f"generated/{filename}"
        parsed = parser_service.parse(source_path)
        content = parsed.get("raw_text", "")
        
        prompt = f"Analyze the following generated content. Validate if it is complete, contains no placeholder sections, and looks like a finalized document. Also check if citations exist if applicable. Reply in exactly this JSON format: {{'status': 'passed' or 'failed', 'report': 'detailed reasoning'}}.\n\nContent:\n{content[:3000]}"
        
        try:
            result = gemini_service.generate_json(prompt)
            import json
            data = json.loads(result.strip("```json").strip("```").strip())
            return data
        except Exception as e:
            return {
                "status": "failed",
                "report": f"Validation parsing failed: {str(e)}"
            }
