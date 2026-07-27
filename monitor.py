from config import SITES
from telegram import send
from state import load,save

from monitors.sepang import check as check_sepang
from monitors.f1tickets import check as check_f1

CHECKERS={
    "sepang":check_sepang,
    "f1tickets":check_f1
}


def main():

    state=load()

    changed=False

    for name,checker in CHECKERS.items():

        current=checker(SITES[name])

        previous=state.get(name,[])

        if current!=previous:

            changed=True

            state[name]=current

            for event in current:

                if event["button"]:

                    send(
f"""🏁 Formula 1 Ticket Update

Website:
{name}

Button detected:
{SITES[name]["button"]}

{textwrap.shorten(event["title"],300)}

{SITES[name]["url"]}
"""
                    )

    if changed:
        save(state)


if __name__=="__main__":
    import textwrap
    main()