import json
import os

FILE="state.json"


def load():

    if not os.path.exists(FILE):
        return {}

    with open(FILE) as f:
        return json.load(f)


def save(data):

    with open(FILE,"w") as f:
        json.dump(data,f,indent=2)