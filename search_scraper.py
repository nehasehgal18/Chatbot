import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import os

def google_search(query):

    url = "https://www.google.com/search"
    
    # Used a custom User-Agent to mimic a real browser to avoid immediate blocking
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    params = {
        "q": query,
        "num": 5 
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    results = []

    # Common selector for an organic search result block
    search_results = soup.select(".tF2Cxc") or soup.select(".g")

    for result_div in search_results:
        link_tag = result_div.select_one("a")
        title_tag = result_div.select_one("h3")
        
        snippet_tag = result_div.select_one(".VwiC3b") 

        title = title_tag.get_text() if title_tag else "No Title Found"
        link_href = link_tag.get('href') if link_tag else None
        snippet = snippet_tag.get_text() if snippet_tag else "No snippet available."

        final_link = None
        if link_href and link_href.startswith('/url?q='):
            # Extracting the actual URL from the 'q' parameter
            parsed_url = urlparse(link_href)
            query_params = parse_qs(parsed_url.query)
            final_link = query_params.get('q', [None])[0]
        elif link_href and link_href.startswith('http'):
             final_link = link_href
        
        if final_link and "google.com" not in final_link and final_link not in [r["link"] for r in results]:
            results.append({
                "title": title,
                "link": final_link,
                "snippet": snippet
            })
        
        if len(results) >= 5: # Stop after 5 results
            break

    return results
