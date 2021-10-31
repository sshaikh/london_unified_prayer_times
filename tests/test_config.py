import datetime
from zoneinfo import ZoneInfo
from london_unified_prayer_times import config
from london_unified_prayer_times import constants


ck = constants.ConfigKeys


def test_build_config():
    json = config.default_config_json
    bconfig = config.build_config(json)
    assert len(bconfig) == len(json)
    assert bconfig[ck.TIMEZONE] == ZoneInfo('Europe/London')
    assert bconfig[ck.CACHE_EXPIRY] == datetime.timedelta(weeks=2)


def test_reload_config():
    cfg = config.load_config(None)
    backup = cfg[ck.DEFAULT_TIMES]
    cfg[ck.DEFAULT_TIMES] = []
    cfg = config.load_config(None)
    assert cfg[ck.DEFAULT_TIMES] == backup
