import datetime
import appdirs
import os
import pickle
from freezegun import freeze_time
from london_unified_prayer_times import cache
from london_unified_prayer_times import config
from london_unified_prayer_times import constants
from . import test_timetable


tk = constants.TimetableKeys
ck = constants.ConfigKeys
pickle_filename = 'pytest'


def assert_timetable_components(data, name, url, size):
    assert data[tk.NAME] == name
    assert data[tk.SETUP][tk.SOURCE] == url
    assert len(data[tk.DATES]) == size
    day = data[tk.DATES][datetime.date(2021, 10, 2)]
    assert day[tk.ISLAMIC_DATES][tk.TODAY] == (1443, "Safar", 25)
    assert day[tk.ISLAMIC_DATES][tk.TOMORROW] == (1443, "Safar", 26)
    assert (day[tk.TIMES]['Sunrise'] ==
            test_timetable.create_utc_datetime(2021, 10, 2, 6, 0))
    assert data[tk.SETUP][tk.CONFIG] == config.default_config


def assert_timetable(data, timetable):
    assert_timetable_components(data,
                                timetable[tk.NAME],
                                timetable[tk.SETUP][tk.SOURCE],
                                len(timetable[tk.DATES]))


def test_cache_timetable(three_day_timetable):
    appname = "london_unified_prayer_times"
    cache_dir = appdirs.user_cache_dir(appname)

    cache.cache_timetable(three_day_timetable)

    cache_file = cache_dir + '/pytest.pickle'
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
    cache_file = appdirs.user_cache_dir(appname) + '/pytest.pickle'
    try:
        os.remove(cache_file)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


def test_init_timetable(three_unsorted_days_mock):
    url = ("https://mock.location.com/lupt")
    data = cache.init_timetable(pickle_filename,
                                url,
                                config.default_config)
    assert_timetable_components(data, pickle_filename, url, 3)


def test_refresh_timetable(three_day_timetable, three_unsorted_days_mock):
    data = cache.refresh_timetable(three_day_timetable)
    assert_timetable(data, three_day_timetable)


def test_refresh_timetable_by_name(three_day_timetable,
                                   three_unsorted_days_mock,
                                   cached_timetable_mock):
    data = cache.refresh_timetable_by_name(three_day_timetable[tk.NAME])
    assert_timetable(data, three_day_timetable)


def help_auto_refresh(tt, week_delta):
    faketime = (datetime.datetime(2021, 10, 15, 15, 15, 15) +
                datetime.timedelta(weeks=week_delta))
    tt[tk.STATS][tk.LAST_UPDATED] = faketime


@freeze_time("2021-10-15 15:15:15")
def test_refresh_timetable_on_load(three_day_timetable,
                                   cached_timetable_mock,
                                   refresh_cached_timetable_mock):

    help_auto_refresh(three_day_timetable, -4)

    delta = datetime.timedelta(weeks=2)
    cache.load_timetable('test', delta)

    assert cache.refresh_timetable.called


@freeze_time("2021-10-15 15:15:15")
def test_no_refresh_timetable_on_load(three_day_timetable,
                                      cached_timetable_mock,
                                      refresh_cached_timetable_mock):

    help_auto_refresh(three_day_timetable, -1)

    delta = datetime.timedelta(weeks=2)
    cache.load_timetable('test', delta)

    assert not cache.refresh_timetable.called


@freeze_time("2021-10-15 15:15:15")
def test_default_refresh_timetable_on_load(three_day_timetable,
                                           cached_timetable_mock,
                                           refresh_cached_timetable_mock):

    help_auto_refresh(three_day_timetable, -1)

    cache.load_timetable('test', None)

    assert not cache.refresh_timetable.called
