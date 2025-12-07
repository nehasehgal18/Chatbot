from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from intent_classifier import predict_intent
from search_api import google_search
from utils import open_site


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
async def chat(data: dict):
    query = data["query"].lower().strip()
    intent = predict_intent(query).lower().strip()

    # -----------------------------
    # INTENT HANDLING
    # -----------------------------

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

    # -----------------------------
    # OPEN WEBSITE (Improved)
    # -----------------------------
    if intent == "open_website":
        # clean domain extraction
        cleaned = (
            query.replace("open", "")
                 .replace("website", "")
                 .replace("site", "")
                 .strip()
        )

        # If user says: open youtube → youtube.com
        if cleaned:
            return {"response": open_site(cleaned)}
        else:
            return {"response": "Which website should I open?"}

    # -----------------------------
    # NEWS INTENT (NEW)
    # -----------------------------
    if intent == "news":
        results = google_search("latest news today")
        return {"response": results}

    # -----------------------------
    # GOOGLE SEARCH INTENT
    # -----------------------------
    if intent == "search_query":
        results = google_search(query)
        return {"response": results}

    # -----------------------------
    # DEFAULT FALLBACK
    # -----------------------------
    return {"response": "I didn’t understand. Try again!"}


