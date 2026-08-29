import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import shutil
from pathlib import Path
from dotenv import load_dotenv

from agents.supervisor import SupervisorAgent

load_dotenv()

app = FastAPI(title="Enterprise Multi-Agent AI Chatbot", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
GENERATED_DIR = Path("generated")
KNOWLEDGE_DIR = Path("knowledge_base")
UPLOAD_DIR.mkdir(exist_ok=True)
GENERATED_DIR.mkdir(exist_ok=True)
KNOWLEDGE_DIR.mkdir(exist_ok=True)

supervisor_agent = SupervisorAgent()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class GenerateRequest(BaseModel):
    session_id: str
    target_format: str # 'docx' or 'pptx'
    template_filename: Optional[str] = None

class EditRequest(BaseModel):
    session_id: str
    instruction: str
    target_filename: str

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    uploaded_files = []
    for file in files:
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Trigger Ingestion
        supervisor_agent.ingest_file(str(file_path))
        
        uploaded_files.append(file.filename)
    return {"message": "Files uploaded successfully", "files": uploaded_files}

@app.post("/chat")
async def chat(request: ChatRequest):
    response = supervisor_agent.process_chat(request.message, request.session_id)
    return {"response": response}

@app.post("/generate")
async def generate(request: GenerateRequest):
    result = supervisor_agent.generate_artifact(request.session_id, request.target_format, request.template_filename)
    return result

@app.post("/edit")
async def edit(request: EditRequest):
    result = supervisor_agent.edit_artifact(request.session_id, request.instruction, request.target_filename)
    return result

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = GENERATED_DIR / filename
    if file_path.exists():
        return FileResponse(path=file_path, filename=filename)
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/history")
async def history(session_id: str = "default"):
    history = supervisor_agent.get_history(session_id)
    return {"history": history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
