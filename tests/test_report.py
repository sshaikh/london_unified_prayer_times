import pytz
from datetime import date
from datetime import datetime


from london_unified_prayer_times import report


def test_timetable_info(three_day_timetable):
    ret = report.show_info(three_day_timetable)
    assert '3 dates available between 2020-10-01 and 2020-10-03' in ret
    assert 'the following times:\n\nfajr' in ret


def test_show_day(three_day_timetable):
    dt = date.fromisoformat('2020-10-01')
    ret = report.show_day(three_day_timetable, dt, None,
                          None, False, pytz.timezone('Europe/London'))
    assert ('Pytest timetable for Oct 01 (14 Safar 1442):\n\n'
            'fajr:      05:31') in ret


def test_show_day_replace(three_day_timetable):
    dt = date.fromisoformat('2020-10-01')
    rs = [('fajr', 'jraf')]
    ret = report.show_day(three_day_timetable, dt, False,
                          rs, False, pytz.timezone('Europe/London'))
    assert ('Pytest timetable for Oct 01 (14 Safar 1442):\n\n'
            'jrafbegins:      05:31') in ret


def test_show_day_time_filter(three_day_timetable):
    dt = date.fromisoformat('2020-10-01')
    use_times = ['zuhrbegins']
    ret = report.show_day(three_day_timetable, dt, use_times,
                          None, False, pytz.timezone('Europe/London'))
    assert 'Pytest timetable for Oct 01 (14 Safar 1442):\n\nzuhr:' in ret


def test_show_day_am(three_day_timetable):
    dt = date.fromisoformat('2020-10-01')
    ret = report.show_day(three_day_timetable, dt, None,
                          None, True, pytz.timezone('Europe/London'))
    assert ('Pytest timetable for Oct 01 (14 Safar 1442):\n\n'
            'fajr:       5:31 am') in ret


def test_show_day_tz(three_day_timetable):
    dt = date.fromisoformat('2020-10-01')
    ret = report.show_day(three_day_timetable, dt, None,
                          None, False, pytz.timezone('CET'))
    assert ('Pytest timetable for Oct 01 (14 Safar 1442):\n\n'
            'fajr:      06:31') in ret


def test_show_calendar(three_day_timetable):
    ret = report.show_calendar(three_day_timetable, 2020, 10, None, None,
                               False, pytz.timezone('Europe/London'))
    assert ('Pytest timetable for October 2020 (Safar 1442):\n\n') in ret
    assert 'date        islamic date    fajr' in ret
    assert '   2 FRI    15 Safar        05:32' in ret


def test_now_next(three_day_timetable):
    tz = pytz.timezone('Europe/London')
    t = datetime(2020, 10, 2, 6).astimezone(tz)
    ret = report.now_and_next(three_day_timetable, t, False,
                              ['fajrbegins', 'zuhrbegins'], None,
                              False, tz)
    assert ('fajr was 28 minutes ago\n'
            'zuhr is 6 hours from now') in ret


def test_now_next_iso(three_day_timetable):
    tz = pytz.timezone('Europe/London')
    t = datetime(2020, 10, 2, 6).astimezone(tz)
    ret = report.now_and_next(three_day_timetable, t, True,
                              ['fajrbegins', 'zuhrbegins'], None,
                              False, tz)
    assert ('fajr 05:32\n'
            'zuhr 12:55') in ret
