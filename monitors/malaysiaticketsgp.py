import requests
from bs4 import BeautifulSoup

BUY_KEYWORDS = ["buy", "book"]


def check(site):

    html = requests.get(
        site["url"],
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    ).text

    soup = BeautifulSoup(html, "lxml")

    for tag in soup.find_all(["a", "button"]):
        if any(kw in tag.get_text(strip=True).lower() for kw in BUY_KEYWORDS):
            return [{"title": "Malaysia GP Tickets", "button": True}]

    return [{"title": "Malaysia GP Tickets", "button": False}]
