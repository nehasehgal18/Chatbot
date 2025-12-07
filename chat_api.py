from fastapi import FastAPI
from pydantic import BaseModel
from search_api import google_search
from utils import predict_intent

app = FastAPI()

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    user_query = request.query

    # Predict intent
    intent = predict_intent(user_query)

    # Intent handling
    if intent == "greeting":
        return {"response": "Hello! How can I help you?"}

    elif intent == "ask_name":
        return {"response": "I am your Smart AI Chatbot!"}

    elif intent == "ask_ability":
        return {"response": "I can search Google and classify your questions using AI."}

    elif intent == "search_query":
        results = google_search(user_query)
        return {"response": results}

    elif intent == "open_website":
        return {"response": "Website opening functionality coming soon!"}

    elif intent == "gratitude":
        return {"response": "You're welcome!"}

    elif intent == "goodbye":
        return {"response": "Goodbye! Have a nice day."}

    else:
        return {"response": "Sorry, I could not understand your query."}
