from datetime import date
from datetime import timedelta
from london_unified_prayer_times import query
from london_unified_prayer_times import constants
from london_unified_prayer_times import timetable
from london_unified_prayer_times import config
from . import test_timetable


tk = constants.TimetableKeys


def test_islamic_date(three_day_timetable):
    today = query.get_islamic_date_today(three_day_timetable,
                                         date(2020, 10, 2))
    assert today == (1442, "Safar", 15)


def test_islamic_date_tomorrow(three_day_timetable):
    tomorrow = query.get_islamic_date_tomorrow(three_day_timetable,
                                               date(2020, 10, 2))
    assert tomorrow == (1442, "Safar", 16)


def test_available_times(three_day_timetable):
    list_times = query.get_available_times(three_day_timetable)

    assert len(list_times) == 12


def test_available_times_empty_timetable():
    tt = timetable.create_empty_timetable('test',
                                          'url',
                                          config.default_config,
                                          config.lupt_schema)
    list_times = query.get_available_times(tt)

    assert len(list_times) == 12


def test_time(three_day_timetable):
    time = query.get_time(three_day_timetable,
                          date(2020, 10, 2),
                          "sunrise")
    assert time == test_timetable.create_utc_datetime(2020, 10, 2, 6, 0)


def test_day(three_day_timetable):
    day = query.get_day(three_day_timetable,
                        date(2020, 10, 2))
    assert (day[tk.TIMES]['sunrise'] ==
            test_timetable.create_utc_datetime(2020, 10, 2, 6, 0))


def test_get_month(three_day_timetable):
    days = query.get_month(three_day_timetable, date(2020, 10, 1))
    assert len(days) == 3
    assert date(2020, 10, 2) in days.keys()


def help_test_current_time(tt, times, query_time, expected):
    ret = query.get_now_and_next(tt, times, query_time)
    assert expected[0][0] == ret[0][0]
    assert expected[0][1] == ret[0][1]
    assert expected[1][0] == ret[1][0]
    assert expected[1][1] == ret[1][1]


def test_get_now_and_next(three_day_timetable):
    help_test_current_time(three_day_timetable,
                           ['fajrbegins', 'zuhrbegins', 'maghribbegins'],
                           test_timetable.create_utc_datetime(2020, 10, 2,
                                                              5, 0),
                           (('fajrbegins',
                             timedelta(minutes=-28)),
                            ('zuhrbegins',
                             timedelta(hours=6, minutes=55))))
    help_test_current_time(three_day_timetable,
                           ['fajrbegins', 'zuhrbegins', 'maghribbegins'],
                           test_timetable.create_utc_datetime(2020, 10, 2,
                                                              14, 0),
                           (('zuhrbegins',
                             timedelta(hours=-2, minutes=-5)),
                            ('maghribbegins',
                             timedelta(hours=3, minutes=38))))
    help_test_current_time(three_day_timetable,
                           ['fajrbegins', 'zuhrbegins', 'maghribbegins'],
                           test_timetable.create_utc_datetime(2020, 10, 2,
                                                              18, 0),
                           (('maghribbegins',
                             timedelta(minutes=-22)),
                            ('fajrbegins',
                             timedelta(hours=10, minutes=34))))
    help_test_current_time(three_day_timetable,
                           ['fajrbegins', 'zuhrbegins', 'maghribbegins'],
                           test_timetable.create_utc_datetime(2020, 10, 2,
                                                              4, 0),
                           (('maghribbegins',
                             timedelta(hours=-10, minutes=-20)),
                            ('fajrbegins',
                             timedelta(minutes=32))))
