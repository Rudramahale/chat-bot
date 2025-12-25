from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from api.predict import predict_intent
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

CONFIDENCE_THRESHOLD = 0.2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_PATH = os.path.join(BASE_DIR, "api", "responses.json")

with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
    RESPONSES = json.load(f)


session_state = {}


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    intent: str
    confidence: float
    reply: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    user_id = req.user_id
    message = req.message.strip().lower()


    if user_id not in session_state:
        session_state[user_id] = {
            "awaiting": None,
            "intent": None
        }


    if session_state[user_id]["awaiting"] == "order_id":
        order_id = message

        intent = session_state[user_id]["intent"]

        session_state[user_id] = {
            "awaiting": None,
            "intent": None
        }

     
        if intent == "order_status":
            reply = f"Your order {order_id} is currently being processed and will be delivered soon."
        elif intent == "refund_request":
            reply = f"Refund for order {order_id} has been initiated. You will receive it in 3–5 business days."
        elif intent == "order_cancellation":
            reply = f"Your order {order_id} has been successfully cancelled."
        else:
            reply = "Thanks for the details. Our team will get back to you."

        return ChatResponse(
            intent=intent,
            confidence=1.0,
            reply=reply
        )


    intent, confidence = predict_intent(message)


    if confidence < CONFIDENCE_THRESHOLD:
        return ChatResponse(
            intent="unknown",
            confidence=confidence,
            reply="Sorry, I couldn’t understand your request. Could you please rephrase?"
        )


    if intent in ["order_status", "refund_request", "order_cancellation"]:
        session_state[user_id]["awaiting"] = "order_id"
        session_state[user_id]["intent"] = intent

        return ChatResponse(
            intent=intent,
            confidence=confidence,
            reply="Please share your order ID to proceed."
        )

    if intent == "technical_issue":
        return ChatResponse(
            intent=intent,
            confidence=confidence,
            reply="Please describe the technical issue you are facing."
        )

    if intent == "billing":
        return ChatResponse(
            intent=intent,
            confidence=confidence,
            reply=RESPONSES.get(intent, "For billing issues, please contact support.")
        )

    return ChatResponse(
        intent=intent,
        confidence=confidence,
        reply=RESPONSES.get(intent, "How can I assist you today?")
    )
