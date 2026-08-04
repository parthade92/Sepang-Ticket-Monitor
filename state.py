import json
import os
import tempfile

FILE = "state.json"


def load():

    if not os.path.exists(FILE):
        return {}

    try:
        with open(FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save(data):

    dir_ = os.path.dirname(os.path.abspath(FILE))

    with tempfile.NamedTemporaryFile("w", dir=dir_, delete=False, suffix=".tmp") as tmp:
        json.dump(data, tmp, indent=2)
        tmp_path = tmp.name

    os.replace(tmp_path, FILE)
