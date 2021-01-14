"""Main module."""

import urllib.request
import json
import jsonschema
from jsonschema import validate


lupt_schema = {
    "$id": "https://github.com/sshaikh/london_unified_prayer_times",
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "data": {
            "type": "array",
            "items": {"$ref": "#/definitions/day"}
        }
    },
    "definitions": {
        "day": {
            "type": "object",
            "required": ["gregoriandate"],
            "properties": {
                "gregoriandate": {
                    "type": "string"
                }
            }
        }
    }
}


def get_json_data(url):
    with urllib.request.urlopen(url) as data:
        json_data = json.loads(data.read().decode())
        return json_data


def validate_json(json):
    try:
        validate(json, lupt_schema)
    except jsonschema.exceptions.ValidationError:
        return False
    return True
