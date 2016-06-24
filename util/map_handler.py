"""
MAP HANDLER
==============
Handles saving/loading/printing of map files.

@author GalenS <galen.scovell@gmail.com>
"""

import json


def save_json(path, content):
    with open(path, 'w') as f:
        json.dump(content, f)


def load_json(path):
    with open(path, 'r') as f:
        content = json.load(f)
    return content


def pretty_print_json(path):
    content = load_json(path)
    print(json.dumps(content, indent=4))
