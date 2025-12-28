from api.session import update_session
import dbOperations as db
import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_PATH = os.path.join(BASE_DIR, "api", "responses.json")

with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
    RESPONSES = json.load(f)

def order_status(session_id,id=None):
    if session[session_id]["status"] == "idel":
        update_session(session_id,"asked_order_id")
        return RESPONSES.get("order_status")

    elif session[session_id]["status"] == "asked_order_id":
        id_status = db.get_status(id)
        if id_status:
            status = db.get_status(id)
            update_session(session_id,"returned order summury")
            return RESPONSES.get(status.lower())
        
        else :
            return RESPONSES.get("order_id_not_found")

def start_chat(session_id, intent):
    if intent.lower() is "order_status":
        order_status(session_id,intent)

    
    