from pathlib import Path
from .generation_agent import GenerationAgent
from .ppt_generation_agent import PPTGenerationAgent
from services.parser import parser_service
from services.gemini import gemini_service
import uuid

class EditingAgent:
    def __init__(self):
        self.gen_agent = GenerationAgent()
        self.ppt_agent = PPTGenerationAgent()

    def edit(self, filename: str, instruction: str) -> str:
        source_path = f"generated/{filename}"
        if not Path(source_path).exists():
            return filename
            
        parsed = parser_service.parse(source_path)
        old_content = parsed.get("raw_text", "")
        
        prompt = f"Here is the content of an existing document:\n\n{old_content}\n\nThe user wants to make the following edit: '{instruction}'.\n\nRewrite the content applying this instruction. Only output the final updated content."
        
        if filename.endswith(".pptx"):
            prompt += "\nFormat output as strictly valid JSON without any markdown code blocks: [{'title': 'Slide 1', 'content': 'bullet points'}, ...]"
            new_content = gemini_service.generate_json(prompt)
            # Re-use PPT logic (we can just call ppt_agent's internal generation if needed, but it's easier to just pass the instruction as context)
            return self.ppt_agent.generate(f"Update this presentation: {old_content}\nInstruction: {instruction}")
            
        else:
            return self.gen_agent.generate(f"Update this document: {old_content}\nInstruction: {instruction}")
