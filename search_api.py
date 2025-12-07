import requests
import os

API_KEY = "AIzaSyBvzkmHKBgXa7fijG4ZLdqREbRSh3V59Qc"
SEARCH_ENGINE_ID = "85d27bd7ae79d4eb1"

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
