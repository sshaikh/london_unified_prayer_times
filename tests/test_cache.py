import pytest
import datetime
import appdirs
import os
import shutil
import pickle
from london_unified_prayer_times import cache
from london_unified_prayer_times import config
from london_unified_prayer_times import constants
from . import test_timetable


tk = constants.TimetableKeys
pickle_filename = constants.PICKLE_FILENAME


def assert_timetable(data, size):
    assert len(data) == 1
    assert len(data[tk.DATES]) == size
    day = data[tk.DATES][datetime.date(2020, 10, 2)]
    assert day[tk.ISLAMIC_DATES][tk.TODAY] == (1442, "Safar", 15)
    assert day[tk.ISLAMIC_DATES][tk.TOMORROW] == (1442, "Safar", 16)
    assert (day[tk.TIMES]['sunrise'] ==
            test_timetable.create_utc_datetime(2020, 10, 2, 6, 0))


def test_cache_timetable(three_day_timetable):
    appname = "london_unified_prayer_times"
    cache_dir = appdirs.user_cache_dir(appname)
    try:
        shutil.rmtree(cache_dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    cache.cache_timetable(three_day_timetable, pickle_filename)

    cache_file = cache_dir + '/timetable.pickle'
    with open(cache_file, 'rb') as cache_json:
        data = pickle.load(cache_json)

        assert_timetable(data, 3)

        try:
            os.remove(cache_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def test_read_cached_timetable(three_day_timetable):
    cache.cache_timetable(three_day_timetable, pickle_filename)
    data = cache.load_cached_timetable(pickle_filename)

    assert_timetable(data, 3)

    appname = "london_unified_prayer_times"
    cache_file = appdirs.user_cache_dir(appname) + '/timetable.pickle'
    try:
        os.remove(cache_file)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


@pytest.mark.vcr()
def test_refresh_timetable():
    url = ("https://mock.location.com/lupt")
    data = cache.refresh_timetable(url,
                                   config.lupt_schema,
                                   config.default_config,
                                   pickle_filename)
    assert_timetable(data, 457)
