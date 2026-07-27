import requests
from bs4 import BeautifulSoup


def check(site):

    html=requests.get(
        site["url"],
        headers={
            "User-Agent":"Mozilla/5.0"
        },
        timeout=30
    ).text

    soup=BeautifulSoup(html,"lxml")

    cards=[]

    for card in soup.find_all():

        text=card.get_text(" ",strip=True)

        if not text:
            continue

        lower=text.lower()

        if any(k in lower for k in site["keywords"]):

            button=site["button"].lower() in lower

            cards.append({
                "title":text[:250],
                "button":button
            })

    return cards