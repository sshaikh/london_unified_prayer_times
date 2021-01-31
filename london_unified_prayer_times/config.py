import json
import importlib.resources as pkg_resources
from . import constants
import pytz


ck = constants.ConfigKeys


def build_config(json):
    config = {}
    for k in ck:
        config[k] = json[k.value]
    config[ck.TIMEZONE] = pytz.timezone(json[ck.TIMEZONE.value])
    return config


default_config_json = json.loads(
    pkg_resources.read_text(__package__, 'default_config.json'))
default_config = build_config(default_config_json)
lupt_schema = json.loads(pkg_resources.read_text(__package__, 'schema.json'))


def load_json(filename):
    with open(filename) as json_file:
        return json.load(json_file)


def safe_load(filename, generator, default):
    return (filename and generator(filename)) or default


def load_schema(filename):
    return safe_load(filename,
                     load_json,
                     lupt_schema)


def load_config(filename):
    return safe_load(filename,
                     lambda f: build_config(load_json(f)),
                     default_config)
