from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.predict import predict_intent, load_model
from pydantic import BaseModel
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_PATH = os.path.join(BASE_DIR, "api", "responses.json")

with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
    RESPONSES = json.load(f)

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    intent: str
    confidence: float
    reply: str

@app.on_event("startup")
def startup_event():
    load_model()

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    intent, confidence = predict_intent(request.message)
    
    reply = RESPONSES.get(intent, RESPONSES["unknown"])
    
    return ChatResponse(
        intent=intent,
        confidence=confidence,
        reply=reply
    )
