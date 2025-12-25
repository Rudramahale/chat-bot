import os 
import joblib
import numpy as np 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


model_path = os.path.join(BASE_DIR,"models","intent_classifier.pkl")
vectorizer_path = os.path.join(BASE_DIR,"models", "tf-idf_vectorizer.pkl")
intent_classifier_path = os.path.join(BASE_DIR,"models", "id_to_intent.pkl")



model = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
id_to_intent = joblib.load(intent_classifier_path)

def predict_intent(user_message):
    
    x = vectorizer.transform([user_message])

    probs = model.predict_proba(x)[0]
    confidence = float(np.max(probs))

    intent_id = int(np.argmax(probs))
    intent = id_to_intent[intent_id]

    return intent, confidence
