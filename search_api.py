import requests
import os
from dotenv import load_dotenv

# Load keys from .env file
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

def google_search(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": API_KEY,
        "cx": SEARCH_ENGINE_ID,
        "num": 5
    }

    response = requests.get(url, params=params).json()

    results = []
    if "items" in response:
        for item in response["items"]:
            results.append({
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            })

    return results
