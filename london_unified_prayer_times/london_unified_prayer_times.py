"""Main module."""

import urllib.request
import json


def get_json_data(url):
    with urllib.request.urlopen(url) as data:
        json_data = json.loads(data.read().decode())
        return json_data
