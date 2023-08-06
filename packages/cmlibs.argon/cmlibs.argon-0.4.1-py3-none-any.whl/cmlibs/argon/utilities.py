import json
import os

from cmlibs.argon.argondocument import ARGON_DOCUMENT_VERSION_KEY


def is_argon_file(filename):
    if not os.path.isfile(filename):
        return False

    try:
        with open(filename, 'r') as f:
            state = f.read()
    except UnicodeDecodeError:
        return False

    try:
        d = json.loads(state)
    except json.JSONDecodeError:
        return False

    if ARGON_DOCUMENT_VERSION_KEY not in d:
        return False

    return True
