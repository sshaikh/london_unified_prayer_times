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
