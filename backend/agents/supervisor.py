import json
from pathlib import Path
from services.gemini import gemini_service
from services.parser import parser_service
from services.vector_store import vector_store
from .research_agent import ResearchAgent
from .rag_agent import RAGAgent
from .generation_agent import GenerationAgent
from .ppt_generation_agent import PPTGenerationAgent
from .validation_agent import ValidationAgent
from .editing_agent import EditingAgent
from .document_agent import DocumentAgent
from .ppt_agent import PPTAgent
from .analysis_agent import AnalysisAgent

class SupervisorAgent:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.rag_agent = RAGAgent()
        self.generation_agent = GenerationAgent()
        self.ppt_generation_agent = PPTGenerationAgent()
        self.validation_agent = ValidationAgent()
        self.editing_agent = EditingAgent()
        self.document_agent = DocumentAgent()
        self.ppt_agent = PPTAgent()
        self.analysis_agent = AnalysisAgent()
        
        # In-memory history for POC
        self.conversations = {}
        self.global_style_guide = ""

    def ingest_file(self, file_path: str):
        parsed = parser_service.parse(file_path)
        raw_text = parsed.get("raw_text", "")
        if raw_text:
            # Chunk and add to FAISS
            chunks = [raw_text[i:i+1000] for i in range(0, len(raw_text), 1000)]
            metadatas = [{"source": Path(file_path).name, "content": chunk} for chunk in chunks]
            vector_store.add_texts(chunks, metadatas)
            
            # Analyze tone/style
            style_desc = self.analysis_agent.analyze_style(raw_text, Path(file_path).name)
            self.global_style_guide += f"\nStyle Guide from {Path(file_path).name}:\n{style_desc}\n"

    def process_chat(self, message: str, session_id: str) -> str:
        if session_id not in self.conversations:
            self.conversations[session_id] = []
            
        self.conversations[session_id].append({"role": "user", "content": message})
        
        # Decide what to do using Gemini
        prompt = f"""
        User Request: {message}
        
        Analyze the request and decide the workflow. 
        Return a JSON object with this structure:
        {{
            "needs_research": true/false,
            "needs_rag": true/false,
            "generate_docx": true/false,
            "generate_pptx": true/false,
            "search_query": "query if research needed else null"
        }}
        """
        
        try:
            decision_str = gemini_service.generate_json(prompt)
            # clean json string if needed
            decision_str = decision_str.strip().strip("```json").strip("```").strip()
            decision = json.loads(decision_str)
        except:
            decision = {"needs_research": True, "needs_rag": True, "generate_docx": False, "generate_pptx": False, "search_query": message}

        context = ""
        
        if decision.get("needs_research"):
            query = decision.get("search_query") or message
            research_data = self.research_agent.research(query)
            context += f"\\nResearch Data:\\n{json.dumps(research_data)}"
            
        if decision.get("needs_rag"):
            rag_data = self.rag_agent.retrieve(message)
            context += f"\\nKnowledge Base Data:\\n{json.dumps(rag_data)}"
            
        # Generate final response based on gathered context
        response_prompt = f"""
        User: {message}
        
        Context:
        {context}
        
        Generate a helpful response summarizing what you found or will do.
        """
        
        final_response = gemini_service.generate_text(response_prompt)
        self.conversations[session_id].append({"role": "assistant", "content": final_response})
        
        return final_response
        
    def generate_artifact(self, session_id: str, target_format: str, template_filename: str = None) -> dict:
        context = "Use recent conversation context."
        if session_id in self.conversations:
            # Send the entire conversation history as context + style guide
            context = json.dumps(self.conversations[session_id])
            
        # Append global style guide
        context += f"\n\n{self.global_style_guide}"
            
        if target_format == "docx":
            filename = self.generation_agent.generate(context, template_filename)
        elif target_format == "pptx":
            filename = self.ppt_generation_agent.generate(context, template_filename)
        else:
            return {"error": "Invalid format"}
            
        # Validate generated artifact
        validation_report = self.validation_agent.validate(filename)
            
        return {"message": "Generated successfully", "filename": filename, "validation": validation_report}

    def edit_artifact(self, session_id: str, instruction: str, target_filename: str) -> dict:
        new_filename = self.editing_agent.edit(target_filename, instruction)
        validation_report = self.validation_agent.validate(new_filename)
        return {"message": "Edited successfully", "filename": new_filename, "validation": validation_report}

    def get_history(self, session_id: str) -> list:
        return self.conversations.get(session_id, [])
