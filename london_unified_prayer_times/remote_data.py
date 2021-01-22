import urllib.request
import json
import jsonschema


def get_json_data(url, schema):
    with urllib.request.urlopen(url) as data:
        json_data = json.loads(data.read().decode())
        jsonschema.validate(json_data, schema)
        return json_data
