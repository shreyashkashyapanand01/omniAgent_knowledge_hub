from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil
import os
from model.ingestion import ingestion_manager
from model.agent import agent_app
from model.code_assistant import code_assistant

app = FastAPI(title="Omni-Agent Knowledge Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models ---
class ChatRequest(BaseModel):
    message: str

class CodeRequest(BaseModel):
    prompt: str

class UrlRequest(BaseModel):
    url: str

# --- Endpoints ---

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    try:
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        
        chunks = ingestion_manager.ingest_pdf(file_location)
        os.remove(file_location)
        return {"status": "success", "chunks": chunks, "message": "PDF ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest/url")
async def ingest_url(request: UrlRequest):
    try:
        result = ingestion_manager.ingest_url(request.url)
        return {"status": "success", "data": result, "message": "URL content ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        inputs = {"question": request.message}
        final_state = agent_app.invoke(inputs)
        return {"response": final_state["generation"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/code")
async def code_gen(request: CodeRequest):
    try:
        response = code_assistant.generate_code(request.prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
