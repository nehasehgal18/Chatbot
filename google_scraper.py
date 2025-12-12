import requests
import random
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

PROXIES = [
    "http://1.1.1.1:80",
    "http://8.8.8.8:8080",
    "http://47.243.55.21:8080",
    "http://103.178.42.14:8181",
    "http://103.163.13.54:8080",
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
    "http://72.10.160.173:8253",
    "http://103.4.146.49:1120",
    "http://200.174.198.32:8888",
    "http://72.10.164.178:2493",
    "http://44.213.1.118:80",
    "http://115.127.179.186:2026",
    "http://59.153.18.174:1120",
    "http://37.228.137.183:10808",
    "http://67.43.236.22:10991",
    "http://52.202.30.36:80",
    "http://193.42.125.156:10808",
    "http://72.10.160.170:13701",
    "http://82.115.24.134:9090",
    "http://200.85.167.254:8080",
    "http://175.208.236.114:8282",
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20200101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
]

def clean_google_link(raw_link: str):
    if raw_link.startswith("/url?q="):
        parsed_url = urlparse(raw_link)
        query_params = parse_qs(parsed_url.query)
        return query_params.get('q', [None])[0]
    return raw_link
    
def google_search_scrape(query: str):
    url = "https://www.google.com/search"

    params = {
        "q": query,
        "num": "10",
        "hl": "en"
    }

    results = []

    for attempt in range(10):
        time.sleep(random.uniform(2, 6))
        
        proxy_choice = random.choice(PROXIES)
        proxy = {"http": proxy_choice, "https": proxy_choice}

        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "identity",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
        }

        try:
            response = requests.get(
                url,
                headers=headers,
                params=params,
                proxies=proxy,
                timeout=5,
            )
            print(f"Attempt {attempt + 1}: Proxy {proxy_choice}, Status Code {response.status_code}")

            if response.status_code != 200 or "Our systems have detected unusual traffic" in response.text:
                continue
            
            soup = BeautifulSoup(response.text, "lxml")

            for h3 in soup.find_all("h3"):
                a = h3.find("a")
                if not a:
                    continue

                link = clean_google_link(a.get("href", ""))
                title = h3.get_text(strip=True)

                if not link or "google.com" in link or "webcache" in link or not link.startswith("http"):
                    continue

                result_container = h3.find_parent("div")
                if result_container:
                    result_container = result_container.find_parent("div")
                if result_container:
                    result_container = result_container.find_parent("li")
                
                snippet = ""
                if result_container:
                    for p_tag in result_container.find_all("p"):
                        text = p_tag.get_text(" ", strip=True)
                        if len(text) > 30:
                            snippet = text
                            break

                results.append({
                    "title": title,
                    "link": link,
                    "snippet": snippet,
                })
            
            if results:
                unique = {}
                for r in results:
                    if r["link"] not in unique:
                        unique[r["link"]] = r
                
                return list(unique.values())[:5]

        except Exception as e:
            print(f"Attempt {attempt + 1}: Proxy {proxy_choice}, Connection Error: {e}")
            continue

    return []