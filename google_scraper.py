import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs # New import for link cleaning
import random
import time # New import for anti-bot delay

# Add more user agents and use random choice for better stability
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20200101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]

def google_scrape(query, limit=5):
    # Add a small, random delay to mimic human behavior
    time.sleep(random.uniform(1, 3))
    
    url = "https://www.google.com/search"
    # Use params for better URL encoding
    params = {"q": query, "hl": "en"} 
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status() # Raise error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser") # Use html.parser
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []

    results = []
    
    # 1. Anchor to the Parent Container (most stable ID)
    parent_container = soup.find('div', id='rso')
    if not parent_container:
        # Fallback needed if #rso changes
        parent_container = soup.find('div', class_='main') or soup 

    # 2. Search for the Structural Pattern (a tag containing an h3)
    for a in parent_container.find_all("a", href=True):
        h3 = a.find("h3")
        if not h3:
            continue  # Not a search result link

        title = h3.get_text(strip=True)
        raw_link = a.get("href")

        # --- CRITICAL CORRECTION: Link Cleaning ---
        final_link = None
        if raw_link and raw_link.startswith('/url?q='):
            # Parse the Google redirect URL to extract the real link
            parsed_url = urlparse(raw_link)
            query_params = parse_qs(parsed_url.query)
            final_link = query_params.get('q', [None])[0]
        elif raw_link and raw_link.startswith('http'):
            final_link = raw_link
        
        # Skip if the link is internal to Google or couldn't be cleaned
        if not final_link or "google.com" in final_link:
            continue

        # Now find snippet text (using your structural sibling approach)
        snippet = ""
        parent_div = a.parent

        # Loop through sibling elements inside the same parent div
        for sib in parent_div.find_all("div", recursive=False):
            text = sib.get_text(" ", strip=True)
            # Heuristic: Avoid very short text to find the actual snippet
            if len(text.split()) > 5:
                snippet = text
                break

        results.append({
            "title": title,
            "link": final_link,
            "snippet": snippet  # CORRECTED KEY NAME for index.html compatibility
        })

        if len(results) >= limit:
            break

    return results