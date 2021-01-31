import datetime
from london_unified_prayer_times import query
from london_unified_prayer_times import constants
from london_unified_prayer_times import timetable
from london_unified_prayer_times import config
from . import test_timetable


tk = constants.TimetableKeys


def test_query_islamic_date(three_day_timetable):
    today = query.get_islamic_date_today(three_day_timetable,
                                         datetime.date(2020, 10, 2))
    assert today == (1442, "Safar", 15)


def test_query_islamic_date_tomorrow(three_day_timetable):
    tomorrow = query.get_islamic_date_tomorrow(three_day_timetable,
                                               datetime.date(2020, 10, 2))
    assert tomorrow == (1442, "Safar", 16)


def test_query_available_times(three_day_timetable):
    list_times = query.get_available_times(three_day_timetable)

    assert len(list_times) == 12


def test_query_available_times_empty_timetable():
    tt = timetable.create_empty_timetable('test',
                                          'url',
                                          config.default_config,
                                          config.lupt_schema)
    list_times = query.get_available_times(tt)

    assert len(list_times) == 12


def test_query_time(three_day_timetable):
    time = query.get_time(three_day_timetable,
                          datetime.date(2020, 10, 2),
                          "sunrise")
    assert time == test_timetable.create_utc_datetime(2020, 10, 2, 6, 0)
