import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import random
import time

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20200101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]

def google_scrape(query, limit=5):
    time.sleep(random.uniform(1, 3))
    
    url = "https://www.google.com/search"
    params = {"q": query, "hl": "en"} 
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser") 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []

    results = []

    search_links = soup.select('a:has(h3)') 

    for link_tag in search_links:
        title_tag = link_tag.find('h3')
        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        raw_link = link_tag.get("href")

        final_link = None
        if raw_link and raw_link.startswith('/url?q='):
            parsed_url = urlparse(raw_link)
            query_params = parse_qs(parsed_url.query)
            final_link = query_params.get('q', [None])[0]
        elif raw_link and raw_link.startswith('http'):
            final_link = raw_link

        if not final_link or "google.com" in final_link or "webcache" in final_link:
            continue

        snippet = ""
        parent_div = link_tag.find_parent("div")
        
        if parent_div:
            for sib_div in parent_div.find_all("div", recursive=False):
                text = sib_div.get_text(" ", strip=True)
                if len(text.split()) > 8 and text not in title:
                    snippet = text
                    break
    
        results.append({
            "title": title,
            "link": final_link,
            "snippet": snippet # CORRECTED KEY NAME for index.html compatibility
        })

        if len(results) >= limit:
            break
    
    unique_results = []
    seen_links = set()
    for res in results:
        if res['link'] not in seen_links:
            unique_results.append(res)
            seen_links.add(res['link'])

    return unique_results
