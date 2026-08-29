from agents.document_agent import DocumentAgent
from agents.ppt_agent import PPTAgent

class ParserService:
    def __init__(self):
        self.doc_agent = DocumentAgent()
        self.ppt_agent = PPTAgent()
        
    def parse(self, file_path: str):
        if file_path.endswith('.docx'):
            return self.doc_agent.analyze_docx(file_path)
        elif file_path.endswith('.pdf'):
            return self.doc_agent.analyze_pdf(file_path)
        elif file_path.endswith('.pptx'):
            return self.ppt_agent.analyze_pptx(file_path)
        return {"error": "Unsupported format"}

parser_service = ParserService()
