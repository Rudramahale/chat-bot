from api.session import update_session, session
from api import dbOperations as db
import os
import json
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESPONSES_PATH = os.path.join(BASE_DIR, "api", "responses.json")

with open(RESPONSES_PATH, "r", encoding="utf-8") as f:
    RESPONSES = json.load(f)

def order_status(session_id):
    if session[session_id]["status"] == "idle":
        update_session(session_id,"asked_order_id")
        return RESPONSES.get("order_status")

    elif session[session_id]["status"] == "asked_order_id":
        id_status = db.get_id(session[session_id]["message"])
        
        if id_status:
            session[session_id]["data"] = db.get_details(session[session_id]["message"])
            status = session[session_id]["data"][0]["order_status"]
            status = status.lower()
            update_session(session_id,"idle")
            return RESPONSES.get(status)
        else :
            update_session(session_id,"idle")
            return RESPONSES.get("order_id_not_found")

def refund_request(session_id):
    if session[session_id]["status"] == "idle":
        update_session(session_id,"asked_order_id")
        return RESPONSES.get("refund_request") 

    elif session[session_id]["status"] == "asked_order_id":
        id_status = db.get_id(session[session_id]["message"])
        if id_status:
            session[session_id]["data"] = db.get_details(session[session_id]["message"])
            status = session[session_id]["data"][0]["order_status"]
            if status != "DELIVERED":
                reply = RESPONSES.get("refund_reconformation")
                reply = reply.format(order_status=status)
                return reply
            else :
                update_session(session_id,"idle")
                return RESPONSES.get("NO_refund")
        else :
            update_session(session_id,"idle")
            return RESPONSES.get("order_id_not_found")


        

def start_chat(session_id, intent):
    if intent.lower() == "order_status":
        return order_status(session_id)
    elif intent.lower() == "refund_request":
        return refund_request(session_id)
    return RESPONSES.get("unknown")

    
    