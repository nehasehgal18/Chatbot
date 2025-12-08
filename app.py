from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from intent_classifier import predict_intent
from search_api import google_search
from utils import open_site


class ChatRequest(BaseModel):
    query: str


app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(data: ChatRequest):
    query = data.query.lower().strip()
    intent = predict_intent(query).lower().strip()

    # Greeting
    if intent == "greeting":
        return {"response": "Hello! How can I help you?"}

    # Ask Name
    if intent == "ask_name":
        return {"response": "I am your Google Search Chatbot 🤖"}

    # Ask Ability
    if intent == "ask_ability":
        return {"response": "I can search anything on Google. Just type your query!"}

    # Goodbye
    if intent == "goodbye":
        return {"response": "Goodbye! Take care 😊"}

    # Gratitude
    if intent == "gratitude":
        return {"response": "You're welcome! 😊"}

    # OPEN WEBSITE
    if intent == "open_website":
        cleaned = (
            query.replace("open", "")
                 .replace("website", "")
                 .replace("site", "")
                 .strip()
        )
        if cleaned:
            return {"response": open_site(cleaned)}
        else:
            return {"response": "Which website should I open?"}

    # NEWS
    if intent == "news":
        results = google_search("latest news today")
        return {"response": results}

    # SEARCH GOOGLE
    if intent == "search_query":
        results = google_search(query)
        return {"response": results}

    # DEFAULT
    return {"response": "I didn’t understand. Try again!"}
