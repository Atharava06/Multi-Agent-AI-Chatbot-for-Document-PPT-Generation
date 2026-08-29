import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

class GeminiService:
    def __init__(self, model_name="gemini-3.5-flash-lite"):
        self.model = genai.GenerativeModel(model_name)

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating text: {str(e)}"
    
    def generate_json(self, prompt: str) -> str:
        # Ask model to output strict JSON
        full_prompt = prompt + "\n\nOutput ONLY valid JSON without any markdown formatting."
        return self.generate_text(full_prompt)

gemini_service = GeminiService()
