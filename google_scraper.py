import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": 
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    
    "Accept-Language": "en-US,en;q=0.9",
}

def google_scrape(query):
    url = "https://www.google.com/search"
    params = {"q": query}

    response = requests.get(url, params=params, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    for result_block in soup.find_all("div"):
        link_tag = result_block.find("a")
        title_tag = result_block.find("h3")

        if link_tag and title_tag:
            link = link_tag.get("href")
            title = title_tag.get_text(strip=True)

            # Snippet: find nearby <div> after <h3>
            snippet = ""
            next_div = title_tag.find_next("div")
            if next_div:
                snippet = next_div.get_text(" ", strip=True)

            if link.startswith("/url?"):
                link = "https://www.google.com" + link

            results.append({
                "title": title,
                "link": link,
                "snippet": snippet
            })

    return results[:5]   # return top 5
