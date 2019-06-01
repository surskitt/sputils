import os
import json


def rel_fn(fn):
    dir_name = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(dir_name, fn)


def mock_json(fn):
    with open(rel_fn(fn)) as f:
        return json.load(f)
