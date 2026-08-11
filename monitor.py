import textwrap

from config import SITES
from telegram import send
from state import load, save

from monitors.sepang import check as check_sepang
from monitors.f1tickets import check as check_f1
from monitors.malaysiaticketsgp import check as check_malaysia

CHECKERS = {
    "sepang": check_sepang,
    "f1tickets": check_f1,
    "malaysiaticketsgp": check_malaysia
}


def main():

    state = load()

    changed = False

    for name, checker in CHECKERS.items():

        try:
            current = checker(SITES[name])
        except Exception as e:
            print(f"[{name}] scrape failed: {e}")
            continue

        previous = state.get(name, [])

        if current != previous:

            changed = True

            state[name] = current

            for event in current:

                if event["button"]:

                    try:
                        send(
f"""🏁 Formula 1 Ticket Update

Website:
{name}

Button detected:
{SITES[name]["button"]}

{textwrap.shorten(event["title"], 300)}

{SITES[name]["url"]}
"""
                        )
                    except Exception as e:
                        print(f"[{name}] telegram failed: {e}")

    if changed:
        save(state)


if __name__ == "__main__":
    main()
