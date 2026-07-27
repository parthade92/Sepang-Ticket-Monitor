import json
import os
import re
import requests
from bs4 import BeautifulSoup

URL = "https://www.sepangcircuit.com/ticketing"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

STATE_FILE = "state.json"


def send_telegram(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=30,
    )


def fetch_page():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/138 Safari/537.36"
           #"AppleWebKit/537.36 Chrome/138 Safari/537.36"
        )
    }

    r = requests.get(URL, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def extract_titles(html):
    soup = BeautifulSoup(html, "lxml")

    titles = set()

    # Find headings
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "strong"]):
        text = tag.get_text(" ", strip=True)

        if len(text) < 4:
            continue

        titles.add(text)

    # Find image alt text
    for img in soup.find_all("img"):
        alt = img.get("alt", "").strip()
        if len(alt) > 4:
            titles.add(alt)

    # Clean
    cleaned = []

    for t in titles:
        t = re.sub(r"\s+", " ", t).strip()

        if len(t) > 4:
            cleaned.append(t)

    return sorted(cleaned)


def load_state():
    if not os.path.exists(STATE_FILE):
        return []

    with open(STATE_FILE, "r") as f:
        return json.load(f)


def save_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=2)


def looks_like_f1(title):
    title = title.lower()

    keywords = [
        "formula 1",
        "formula one",
        "f1",
        "petronas",
        "malaysian grand prix",
        "malaysia grand prix",
    ]

    return any(k in title for k in keywords)


def main():
    html = fetch_page()

    current = extract_titles(html)

    previous = load_state()

    new_titles = [x for x in current if x not in previous]

    print("Current titles:")
    for t in current:
        print("-", t)

    if new_titles:
        print("\nNew titles found:")
        for t in new_titles:
            print("-", t)

            if looks_like_f1(t):
                send_telegram(
                    f"🏁 Formula 1 ticket listing detected!\n\n{t}\n\n{URL}"
                )

    else:
        print("No new titles.")

    save_state(current)


if __name__ == "__main__":
    main()