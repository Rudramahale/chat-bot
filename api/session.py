from datetime import datetime

session = {}

def create_session(session_id:str,intent:str,mes:str):
    session[session_id]={
        "intent":intent,
        "status":"idle",
        "data":None,
        "updated_at":datetime.now(),
        "message":mes,
        "order_id":None
    }
    return session[session_id]


def update_session(session_id:str,status:str):
    if session_id not in session:
        return None
    session[session_id]["status"] = status
    session[session_id]["updated_at"] = datetime.now()
    return session[session_id] 