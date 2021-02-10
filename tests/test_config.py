import pytest
import jsonschema
import pytz
import datetime
from london_unified_prayer_times import config
from london_unified_prayer_times import constants


ck = constants.ConfigKeys


def test_build_config():
    json = config.default_config_json
    bconfig = config.build_config(json)
    assert len(bconfig) == len(json)
    assert bconfig[ck.TIMEZONE] == pytz.timezone('Europe/London')
    assert bconfig[ck.CACHE_EXPIRY] == datetime.timedelta(weeks=2)


def test_validate_json(single_day):
    assert jsonschema.validate(single_day, config.lupt_schema) is None


def test_invalid_json(bad_json):
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad_json, config.lupt_schema)
