import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs
import random
import time

PROXY_POOL = [
    "http://113.177.204.26:8080", 
    "http://52.188.28.218:3128",
    "http://46.161.6.165:8080",
    "http://74.50.77.58:9090",
    "http://195.158.8.123:3128",
    "http://47.251.57.165:1080",
    "http://185.238.169.111:50080",
    "http://182.53.202.208:8080",
    "http://175.196.233.104:3128",
    "http://18.202.158.161:80", 
]


# List of rotating User-Agents for better stability
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20200101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]

def google_scrape(query, limit=5):
    if PROXY_POOL and "placeholder" not in PROXY_POOL[0]:
        selected_proxy_url = random.choice(PROXY_POOL)
        proxies = {
            "http": selected_proxy_url,
            "https": selected_proxy_url,
        }
    else:
        proxies = None 

    time.sleep(random.uniform(1, 3))
    
    url = "https://www.google.com/search"
    params = {"q": query, "hl": "en"} 
    headers = {"User-Agent": random.choice(USER_AGENTS)}

    try:
        response = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=10)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, "lxml") 
    except requests.exceptions.RequestException as e:
        print(f"Error fetching search results (Proxy/Connection issue): {e}")
        return []

    results = []

    parent_container = soup.find('div', id='rso')
    if not parent_container:
        parent_container = soup 

    for h3_tag in parent_container.find_all('h3'):
        link_tag = h3_tag.find_parent('a') 
        
        if not link_tag or not link_tag.get('href'):
            continue

        title = h3_tag.get_text(strip=True)
        raw_link = link_tag.get("href")

        final_link = None
        if raw_link and raw_link.startswith('/url?q='):
            # Extract the real URL from the Google redirect path
            parsed_url = urlparse(raw_link)
            query_params = parse_qs(parsed_url.query)
            final_link = query_params.get('q', [None])[0]
        elif raw_link and raw_link.startswith('http'):
            final_link = raw_link
        
        # Skip internal Google links
        if not final_link or "google.com" in final_link or "webcache" in final_link:
            continue

        result_block = link_tag.find_parent('div') 
        
        snippet = ""
        if result_block:
            # Find a div/span that is long enough to be the snippet
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

    # Deduplication
    unique_results = []
    seen_links = set()
    for res in results:
        if res['link'] not in seen_links:
            unique_results.append(res)
            seen_links.add(res['link'])

    return unique_results