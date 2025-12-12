from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google_scraper import google_search_scrape
from utils import open_site

app = FastAPI()

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
    return FileResponse("index.html")

@app.post("/chat")
def chat(data: ChatRequest):
    query = data.query.lower().strip()

    # If user wants to open website
    if query.startswith("open") or query.startswith("go to"):
        cleaned = query.replace("open", "").replace("go to", "").replace("website", "").replace("site", "").strip()
        if cleaned:
            return {"response": open_site(cleaned)}

    # Otherwise: Always Google search
    result = google_search_scrape(query)
    return {"response": result}
