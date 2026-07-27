import json
import os
import requests
from bs4 import BeautifulSoup

URL = "https://www.sepangcircuit.com/ticketing"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

KEYWORDS = [
    "formula 1",
    "formula one",
    "f1",
    "bahrain grand prix",
    "grand prix"
]

STATE_FILE = "state.json"


def send(message):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=20,
    )


def load_state():
    if not os.path.exists(STATE_FILE):
        return {"already_notified": False}

    with open(STATE_FILE) as f:
        return json.load(f)


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def fetch_page():
    headers = {
        "User-Agent": (
            "Mozilla/5.0 "
            "(Windows NT 10.0; Win64; x64)"
        )
    }

    r = requests.get(URL, headers=headers, timeout=30)
    r.raise_for_status()
    return r.text


def check():
    html = fetch_page()

    soup = BeautifulSoup(html, "html.parser")

    text = soup.get_text(" ", strip=True).lower()

    for keyword in KEYWORDS:
        if keyword in text:
            return keyword

    return None


def main():
    state = load_state()

    keyword = check()

    if keyword:
        if not state["already_notified"]:
            send(
                "🏁 Formula 1 tickets may be LIVE!\n\n"
                f"Matched keyword: {keyword}\n\n"
                f"{URL}"
            )

            state["already_notified"] = True
            save_state(state)

    else:
        state["already_notified"] = False
        save_state(state)


if __name__ == "__main__":
    main()