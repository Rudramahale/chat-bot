import os 
import joblib
import numpy as np 

print("Initializing predict module...")

state = {
    'model': None,
    'vectorizer': None,
    'id_to_intent': None
}

def load_model():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    model_path = os.path.join(BASE_DIR,"exp_models","intent_classifier.pkl")
    vectorizer_path = os.path.join(BASE_DIR,"exp_models", "tf-idf_vectorizer2.pkl")
    intent_classifier_path = os.path.join(BASE_DIR,"exp_models", "id_to_intent2.pkl")

    try:
        state['model'] = joblib.load(model_path)
        print("Model loaded successfully.")
        state['vectorizer'] = joblib.load(vectorizer_path)
        print("Vectorizer loaded successfully.")
        state['id_to_intent'] = joblib.load(intent_classifier_path)
        print("Intent classifier loaded successfully.")
    except Exception as e:
        print(f"Error loading models: {e}")

def predict_intent(user_message):
    print(f"Predicting intent for: {user_message}")
    
    model = state['model']
    vectorizer = state['vectorizer']
    id_to_intent = state['id_to_intent']

    if model is None:
        print("Error: Model is None inside predict_intent")
        return "unknown", 0.0
        
    try:
        x = vectorizer.transform([user_message])

        probs = model.predict_proba(x)[0]
        confidence = float(np.max(probs))

        intent_id = int(np.argmax(probs))
        intent = id_to_intent[intent_id]

        print(f"Predicted: {intent} ({confidence})")
        return intent, confidence
    except Exception as e:
        print(f"Prediction Error: {e}")
        return "unknown", 0.0
