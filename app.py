from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from intent_classifier import predict_intent
# --- CORRECTED IMPORT ---
from search_scraper import google_search 
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

class ChatRequest(BaseModel):
    query: str

@app.get("/")
def home():
    # serve index.html at root
    return FileResponse("index.html")

@app.post("/chat")
async def chat(data: ChatRequest):
    query = data.query.lower().strip()
    intent = predict_intent(query).lower().strip()

    if intent == "greeting":
        return {"response": "Hello! How can I help you?"}

    if intent == "ask_name":
        # Restored "Google Search Chatbot"
        return {"response": "I am your Google Search Chatbot 🤖"}

    if intent == "ask_ability":
        # Restored reference to Google
        return {"response": "I can search anything on Google. Just type your query!"}

    if intent == "goodbye":
        return {"response": "Goodbye! Take care 😊"}

    if intent == "gratitude":
        return {"response": "You're welcome! 😊"}

    if intent == "open_website":
        cleaned = query.replace("open", "").replace("website", "").replace("site", "").strip()
        if cleaned:
            return {"response": open_site(cleaned)}
        return {"response": "Which website should I open?"}

    if intent == "news":
        # --- CORRECTED FUNCTION CALL ---
        return {"response": google_search("latest news today")}

    if intent == "search_query":
        # --- CORRECTED FUNCTION CALL ---
        return {"response": google_search(query)}

    return {"response": "I didn’t understand. Try again!"}