"""Main module."""

import urllib.request
import json
import jsonschema
import importlib.resources as pkg_resources


lupt_schema = json.loads(pkg_resources.read_text(__package__, 'schema.json'))


def get_json_data(url):
    with urllib.request.urlopen(url) as data:
        json_data = json.loads(data.read().decode())
        jsonschema.validate(json_data, lupt_schema)
        return json_data
