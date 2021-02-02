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
ck = constants.ConfigKeys
pickle_filename = constants.PICKLE_FILENAME


def assert_timetable_components(data, name, url, size):
    assert data[tk.NAME] == name
    assert data[tk.SOURCE] == url
    assert len(data[tk.DATES]) == size
    day = data[tk.DATES][datetime.date(2020, 10, 2)]
    assert day[tk.ISLAMIC_DATES][tk.TODAY] == (1442, "Safar", 15)
    assert day[tk.ISLAMIC_DATES][tk.TOMORROW] == (1442, "Safar", 16)
    assert (day[tk.TIMES]['sunrise'] ==
            test_timetable.create_utc_datetime(2020, 10, 2, 6, 0))
    assert data[tk.CONFIG] == config.default_config
    assert data[tk.SCHEMA] == config.lupt_schema


def assert_timetable(data, timetable):
    assert_timetable_components(data,
                                timetable[tk.NAME],
                                timetable[tk.SOURCE],
                                len(timetable[tk.DATES]))


def test_cache_timetable(three_day_timetable):
    appname = "london_unified_prayer_times"
    cache_dir = appdirs.user_cache_dir(appname)
    try:
        shutil.rmtree(cache_dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    cache.cache_timetable(three_day_timetable)

    cache_file = cache_dir + '/default.pickle'
    with open(cache_file, 'rb') as cache_json:
        data = pickle.load(cache_json)

        assert_timetable(data, three_day_timetable)

        try:
            os.remove(cache_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def test_read_cached_timetable(three_day_timetable):
    cache.cache_timetable(three_day_timetable)
    data = cache.load_cached_timetable(pickle_filename)

    assert_timetable(data, three_day_timetable)

    appname = "london_unified_prayer_times"
    cache_file = appdirs.user_cache_dir(appname) + '/default.pickle'
    try:
        os.remove(cache_file)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def test_init_timetable(three_unsorted_days_mock):
    url = ("https://mock.location.com/lupt")
    data = cache.init_timetable(pickle_filename,
                                url,
                                config.default_config,
                                config.lupt_schema)
    assert_timetable_components(data, pickle_filename, url, 3)


def test_refresh_timetable(three_day_timetable, three_unsorted_days_mock):
    data = cache.refresh_timetable(three_day_timetable)
    assert_timetable(data, three_day_timetable)


def test_refresh_timetable_by_name(three_day_timetable,
                                   three_unsorted_days_mock,
                                   cached_timetable_mock):
    data = cache.refresh_timetable_by_name(three_day_timetable[tk.NAME])
    assert_timetable(data, three_day_timetable)
