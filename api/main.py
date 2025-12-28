from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.predict import predict_intent, load_model
from api.chat import start_chat
from api.session import create_session, session
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    intent = None
    confidence = None
 
    if request.session_id not in session:
        intent, confidence = predict_intent(request.message)
        create_session(request.session_id, intent,request.message)
    else:
        intent = session[request.session_id]["intent"]
        session[request.session_id]["message"] = request.message
        confidence = 1.0

    reply = start_chat(request.session_id,intent)
    
    return ChatResponse(
        intent=intent,
        confidence=confidence,
        reply=reply
    )

