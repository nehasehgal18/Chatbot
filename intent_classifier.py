import pickle

with open("models/intent_model.pkl", "rb") as f:
    model, vectorizer = pickle.load(f)

def predict_intent(text):
    features = vectorizer.transform([text])
    return model.predict(features)[0]
