import requests
from bs4 import BeautifulSoup

F1_KEYWORDS = [
    "f1",
    "formula 1",
    "formula1",
    "petronas",
    "formula 1 gulf air bahrain grand prix in malaysia 2026"
]


def check(site):

    html = requests.get(
        site["url"],
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=30
    ).text

    soup = BeautifulSoup(html, "lxml")

    events = []

    for a in soup.find_all("a"):

        btn = a.find("button")
        if not btn or site["button"].lower() not in btn.get_text(strip=True).lower():
            continue

        title = a.get_text(" ", strip=True).replace(btn.get_text(strip=True), "").strip()

        if not any(kw in title.lower() for kw in F1_KEYWORDS):
            continue

        href = a.get("href", "")
        # href points to an overview page until tickets actually go on sale
        bookable = href not in ("#", "", None) and "overview" not in href

        events.append({
            "title": title,
            "button": bookable
        })

    return events
