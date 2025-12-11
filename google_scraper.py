import requests
from bs4 import BeautifulSoup

def google_scrape(query):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    url = "https://www.google.com/search?q=" + query.replace(" ", "+")

    response = requests.get(url, headers=headers, timeout=5)
    soup = BeautifulSoup(response.text, "lxml")

    results = []

    for block in soup.find_all("div"):
        a = block.find("a", href=True)
        if not a:
            continue

        h3 = a.find("h3")
        if not h3:
            continue

        title = h3.get_text(strip=True)
        link = a["href"]

        snippet = ""
        next_div = block.find("div")
        if next_div:
            snippet = next_div.get_text(" ", strip=True)

        results.append({
            "title": title,
            "link": link,
            "description": snippet
        })

    # remove duplicates
    unique = {}
    for r in results:
        if r["link"] not in unique:
            unique[r["link"]] = r

    results = list(unique.values())

    if len(results) == 0:
        return [{
            "title": "No results found",
            "link": "",
            "description": ""
        }]

    return results[:8]
