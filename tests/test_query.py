from datetime import date
from london_unified_prayer_times import query
from london_unified_prayer_times import constants
from london_unified_prayer_times import timetable
from london_unified_prayer_times import config
from . import test_timetable


tk = constants.TimetableKeys
ck = constants.ConfigKeys


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


def test_get_info(three_day_timetable):
    tt = three_day_timetable
    data = query.get_info(tt)
    assert data[0] == tt[tk.NAME]
    assert data[1] == tt[tk.SETUP][tk.SOURCE]
    assert data[2] == (tt[tk.STATS][tk.NUMBER_OF_DATES],
                       tt[tk.STATS][tk.MIN_DATE],
                       tt[tk.STATS][tk.MAX_DATE])
    assert data[3] == (tt[tk.STATS][tk.LAST_UPDATED],
                       tt[tk.SETUP][tk.CONFIG][ck.CACHE_EXPIRY])


def test_get_config(three_day_timetable):
    tt = three_day_timetable
    data = query.get_config(tt)
    assert data == (tt[tk.SETUP][tk.CONFIG],
                    tt[tk.SETUP][tk.SCHEMA])


def help_test_now_and_next(tt, times, query_time, expected):
    ret = query.get_now_and_next(tt, times, query_time)
    assert expected[0][0] == ret[0][0]
    assert expected[0][1] == ret[0][1]
    assert expected[1][0] == ret[1][0]
    assert expected[1][1] == ret[1][1]


def test_get_now_and_next(three_day_timetable):
    help_test_now_and_next(three_day_timetable,
                           ['fajrbegins', 'zuhrbegins', 'maghribbegins'],
                           test_timetable.create_utc_datetime(2020, 10, 2,
                                                              5, 0),
                           (('fajrbegins',
                             test_timetable.create_utc_datetime(2020, 10, 2,
                                                                4, 32)),
                            ('zuhrbegins',
                             test_timetable.create_utc_datetime(2020, 10, 2,
                                                                11, 55))))
    help_test_now_and_next(three_day_timetable,
                           ['fajrbegins', 'zuhrbegins', 'maghribbegins'],
                           test_timetable.create_utc_datetime(2020, 10, 2,
                                                              14, 0),
                           (('zuhrbegins',
                             test_timetable.create_utc_datetime(2020, 10, 2,
                                                                11, 55)),
                            ('maghribbegins',
                             test_timetable.create_utc_datetime(2020, 10, 2,
                                                                17, 38))))
    help_test_now_and_next(three_day_timetable,
                           ['fajrbegins', 'zuhrbegins', 'maghribbegins'],
                           test_timetable.create_utc_datetime(2020, 10, 2,
                                                              18, 0),
                           (('maghribbegins',
                             test_timetable.create_utc_datetime(2020, 10, 2,
                                                                17, 38)),
                            ('fajrbegins',
                             test_timetable.create_utc_datetime(2020, 10, 3,
                                                                4, 34))))
    help_test_now_and_next(three_day_timetable,
                           ['fajrbegins', 'zuhrbegins', 'maghribbegins'],
                           test_timetable.create_utc_datetime(2020, 10, 2,
                                                              4, 0),
                           (('maghribbegins',
                             test_timetable.create_utc_datetime(2020, 10, 1,
                                                                17, 40)),
                            ('fajrbegins',
                             test_timetable.create_utc_datetime(2020, 10, 2,
                                                                4, 32))))
