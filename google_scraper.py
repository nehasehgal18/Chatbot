import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import random
import time

# Essential for anti-bot measures
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20200101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]

def google_scrape(query, limit=5):
    # CRITICAL ANTI-BOT: Delay and Rotating User-Agent
    time.sleep(random.uniform(1, 3))
    
    url = "https://www.google.com/search"
    params = {"q": query, "hl": "en"} 
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml") # Using lxml is generally faster/more robust
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []

    results = []

    # 1. Anchor to the main parent container, where all results live
    parent_container = soup.find('div', id='rso')
    if not parent_container:
        # Fallback to the body if #rso is missing
        parent_container = soup 

    # 2. Find the structural pattern: anchor to the H3 and work outwards
    # This is often more reliable than anchoring to the <a>
    for h3_tag in parent_container.find_all('h3'):
        # The <h3> is often a child of the <a> tag, or a sibling of the snippet div.
        
        # Look for the link tag (<a>) that contains this h3
        link_tag = h3_tag.find_parent('a') 
        
        if not link_tag or not link_tag.get('href'):
            continue

        title = h3_tag.get_text(strip=True)
        raw_link = link_tag.get("href")

        # --- CRITICAL FIX: Link Cleaning ---
        final_link = None
        if raw_link and raw_link.startswith('/url?q='):
            parsed_url = urlparse(raw_link)
            query_params = parse_qs(parsed_url.query)
            final_link = query_params.get('q', [None])[0]
        elif raw_link and raw_link.startswith('http'):
            final_link = raw_link
        
        if not final_link or "google.com" in final_link or "webcache" in final_link:
            continue

        # Snippet Extraction: Look in the parent block for descriptive text.
        # Find the main result block (often a common parent <div> for the link/title and snippet).
        result_block = link_tag.find_parent('div') 
        
        snippet = ""
        if result_block:
             # Look for the first <span> or <div> that is long enough and not the title itself
            for text_block in result_block.find_all(['span', 'div']):
                text = text_block.get_text(" ", strip=True)
                if len(text.split()) > 10 and text != title:
                    snippet = text
                    break

        results.append({
            "title": title,
            "link": final_link,
            "snippet": snippet
        })

        if len(results) >= limit:
            break

    # Use a dictionary to remove duplicates based on the final link
    unique_results = []
    seen_links = set()
    for res in results:
        if res['link'] not in seen_links:
            unique_results.append(res)
            seen_links.add(res['link'])

    return unique_results