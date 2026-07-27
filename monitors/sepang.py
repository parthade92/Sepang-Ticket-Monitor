import requests
from bs4 import BeautifulSoup

F1_KEYWORDS = [
    "formula 1",
    "formula one",
    "f1",
    "formula",
    "formula1"
]


def check(site):

    html = requests.get(
        site["url"],
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    ).text

    soup = BeautifulSoup(html, "lxml")

    events = []

    # Only inspect likely event cards
    for card in soup.find_all(["div", "article", "section", "li"]):

        text = card.get_text(" ", strip=True)

        if not text:
            continue

        lower = text.lower()

        # Skip anything that isn't Formula 1
        if not any(keyword in lower for keyword in F1_KEYWORDS):
            continue

        # Only alert if THIS card contains Buy Ticket
        if "buy ticket" not in lower:
            continue

        events.append({
            "title": text[:300],
            "button": True
        })

    return events