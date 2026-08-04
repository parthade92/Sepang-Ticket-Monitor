import requests
from bs4 import BeautifulSoup


def check(site):

    html = requests.get(
        site["url"],
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    ).text

    soup = BeautifulSoup(html, "lxml")

    for card in soup.find_all("div", class_="f1-cc"):

        text = card.get_text(" ", strip=True)
        lower = text.lower()

        if "bahrain" not in lower or "2026" not in lower:
            continue

        button = site["button"].lower() in lower

        return [{"title": text[:300], "button": button}]

    return [{"title": "Bahrain GP 2026 not found", "button": False}]