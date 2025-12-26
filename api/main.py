from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.predict import predict_intent, load_model
from api.conversation_manager import ConversationManager
import json
import os

app = FastAPI(
    title="Customer Support Chatbot API",
    description="Intent-based NLP chatbot using TF-IDF + ML",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIDENCE_THRESHOLD = 0.6

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_PATH = os.path.join(BASE_DIR, "api", "responses.json")

# Load responses
if os.path.exists(RESPONSES_PATH):
    with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
        RESPONSES = json.load(f)
else:
    RESPONSES = {}

# Initialize ConversationManager
conversation_manager = ConversationManager(RESPONSES)

class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    intent: str
    confidence: float
    reply: str

@app.on_event("startup")
def startup_event():
    print("Startup: Loading models...")
    try:
        load_model()
        print("Startup: Models loaded.")
    except Exception as e:
        print(f"Startup Error: {e}")

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    user_id = req.user_id
    message = req.message.strip().lower()

    # Get current state
    state = conversation_manager.get_state(user_id)

    # Determine intent
    if state["awaiting"]:
        # If awaiting input, we don't need to predict intent for this turn
        intent = None
        confidence = 0.0
    else:
        # Predict intent
        intent, confidence = predict_intent(message)
        
        if confidence < CONFIDENCE_THRESHOLD:
            intent = "unknown"

    # Delegate flow handling to manager
    response_data = conversation_manager.handle_flow(user_id, message, intent, confidence)

    return ChatResponse(
        intent=response_data["intent"],
        confidence=response_data["confidence"],
        reply=response_data["reply"]
    )
