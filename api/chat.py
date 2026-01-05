from api.session import update_session, session
from api.predict import predict_intent
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

            if status != "DELIVERED" and status != "CANCELLED" and session[session_id]["data"][0]["payment_mode"] != "COD" :
                reply = RESPONSES.get("refund_reconfirmation")
                reply = reply.format(order_status=status)
                update_session(session_id,"get_confirmation")
                return reply
            elif status == "REFUND_INITIATED" : 
                return RESPONSES.get("refund_already_intiated")
            elif status == "REFUNDED":
                return RESPONSES.get("Already_Refunded")
            else :
                if session[session_id]["data"][0]["payment_mode"] == "COD" :
                    update_session(session_id,"idle")
                    return RESPONSES.get("cod_payment_mode")
                else :
                    reply = RESPONSES.get("NO_refund")
                    reply = reply.format(order_status=status)
                    update_session(session_id,"idle")
                    return reply
        else :
            update_session(session_id,"idle")
            return RESPONSES.get("order_id_not_found")

    elif session[session_id]["status"] == "get_confirmation" :
        conformation,confidence = predict_intent(session[session_id]["message"])
        if confidence < 0.5:
                update_session(session_id,"idle")
                return RESPONSES.get("unknown")
        elif conformation == "confirmation_yes" :
            state = db.update_refund_status(session[session_id]["data"][0]["order_id"])
            if state == True:
                update_session(session_id,"idle")
                return RESPONSES.get("refund_initiated")
            else :
                update_session(session_id,"idle")
                return RESPONSES.get("refund_technical_issue")
        else :
            update_session(session_id,"idle")
            return RESPONSES.get("refund_canceled")


def order_cancellation(session_id):
    if session[session_id]["status"] == "idle":
        update_session(session_id,"asked_order_id")
        return RESPONSES.get("order_cancellation")
    
    elif session[session_id]["status"] == "asked_order_id":
        id_status = db.get_id(session[session_id]["message"])
        if id_status:
            session[session_id]["data"] = db.get_details(session[session_id]["message"])
            status = session[session_id]["data"][0]["order_status"]

            if status != "DELIVERED" and status != "CANCELLED":
                reply = RESPONSES.get("cancellation_reconfirmation")
                reply = reply.format(order_status=status)
                update_session(session_id,"get_cancellation_confirmation")
                return reply
            elif status == "CANCELLED" : 
                update_session(session_id,"idle")
                return RESPONSES.get("order_already_canceled")
            else :
                update_session(session_id,"idle")
                return RESPONSES.get("delivered")
        else :
            update_session(session_id,"idle")
            return RESPONSES.get("order_id_not_found")


    elif session[session_id]["status"] == "get_cancellation_confirmation" :
        conformation,confidence = predict_intent(session[session_id]["message"])
        if confidence < 0.5:
            update_session(session_id,"idle")
            return RESPONSES.get("unknown")
        elif conformation == "confirmation_yes" :
            state = db.update_cancel_order(session[session_id]["data"][0]["order_id"])
            if state == True:
                update_session(session_id,"idle")
                return RESPONSES.get("order_canceled")
            else :
                update_session(session_id,"idle")
                return RESPONSES.get("order_cancellation_technical_issue")
        else :
            update_session(session_id,"idle")
            return RESPONSES.get("order_canceled_rejected")


            
        
        

def start_chat(session_id, intent):
    if intent.lower() == "order_status":
        return order_status(session_id)
    elif intent.lower() == "refund_request":
        return refund_request(session_id)
    elif intent.lower() == "order_cancellation":
        return order_cancellation(session_id)
    elif intent.lower() == "technical_issue":
        return RESPONSES.get("technical_issue")
    else:
        return RESPONSES.get("unknown")

    
    