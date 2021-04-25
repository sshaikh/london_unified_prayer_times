import pytz
from datetime import date
from datetime import datetime


from london_unified_prayer_times import report


def test_timetable_info(three_day_timetable):
    ret = report.show_info(three_day_timetable)
    assert '3 dates available between 2021-10-01 and 2021-10-03' in ret
    assert 'the following times:\n\nFajr' in ret


def test_show_day(three_day_timetable):
    dt = date.fromisoformat('2021-10-01')
    ret = report.show_day(three_day_timetable, dt, None,
                          None, False, pytz.timezone('Europe/London'))
    assert ('Pytest timetable for Oct 01 2021 (24 Safar 1443):\n\n'
            'Fajr:      05:30') in ret


def test_show_day_replace(three_day_timetable):
    dt = date.fromisoformat('2021-10-01')
    rs = [('Fajr', 'Jraf')]
    ret = report.show_day(three_day_timetable, dt, False,
                          rs, False, pytz.timezone('Europe/London'))
    assert ('Pytest timetable for Oct 01 2021 (24 Safar 1443):\n\n'
            'Jraf Begins:      05:30') in ret


def test_show_day_time_filter(three_day_timetable):
    dt = date.fromisoformat('2021-10-01')
    use_times = ['Zuhr Begins']
    ret = report.show_day(three_day_timetable, dt, use_times,
                          None, False, pytz.timezone('Europe/London'))
    assert 'Pytest timetable for Oct 01 2021 (24 Safar 1443):\n\nZuhr:' in ret


def test_show_day_am(three_day_timetable):
    dt = date.fromisoformat('2021-10-01')
    ret = report.show_day(three_day_timetable, dt, None,
                          None, True, pytz.timezone('Europe/London'))
    assert ('Pytest timetable for Oct 01 2021 (24 Safar 1443):\n\n'
            'Fajr:       5:30 am') in ret


def test_show_day_tz(three_day_timetable):
    dt = date.fromisoformat('2021-10-01')
    ret = report.show_day(three_day_timetable, dt, None,
                          None, False, pytz.timezone('CET'))
    assert ('Pytest timetable for Oct 01 2021 (24 Safar 1443):\n\n'
            'Fajr:      06:30') in ret


def test_show_calendar(three_day_timetable):
    ret = report.show_calendar(three_day_timetable, 2021, 10, None, None,
                               False, pytz.timezone('Europe/London'))
    assert ('Pytest timetable for October 2021 (Safar 1443):\n\n') in ret
    assert 'Date        Islamic Date    Fajr' in ret
    assert '   1 FRI    24 Safar        05:30' in ret


def test_now_next(three_day_timetable):
    tz = pytz.timezone('Europe/London')
    t = datetime(2021, 10, 2, 6).astimezone(tz)
    ret = report.now_and_next(three_day_timetable, t, False,
                              ['Fajr Begins', 'Zuhr Begins'], None,
                              False, tz)
    assert ('Fajr was 28 minutes ago\n'
            'Zuhr is 6 hours from now') in ret


def test_now_next_iso(three_day_timetable):
    tz = pytz.timezone('Europe/London')
    t = datetime(2021, 10, 2, 6).astimezone(tz)
    ret = report.now_and_next(three_day_timetable, t, True,
                              ['Fajr Begins', 'Zuhr Begins'], None,
                              False, tz)
    assert ('Fajr 05:32\n'
            'Zuhr 12:55') in ret
