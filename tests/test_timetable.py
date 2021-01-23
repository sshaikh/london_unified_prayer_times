import datetime
import pytz
from london_unified_prayer_times import config
from london_unified_prayer_times import timetable
from london_unified_prayer_times import constants


tk = constants.TimetableKeys
ck = constants.ConfigKeys


def help_test_fix_gregorian_date(sample_string, expected_date):
    tz = pytz.timezone('Europe/London')
    found = timetable.fix_gregorian_date(sample_string, tz)

    assert found == expected_date


def test_fix_gregorian_date_bst():
    sample = "2020-10-01T23:00:00.000Z"
    expected = datetime.date(2020, 10, 2)
    help_test_fix_gregorian_date(sample, expected)


def test_fix_gregorian_date_gmt():
    sample = "2020-11-01T00:00:00.000Z"
    expected = datetime.date(2020, 11, 1)
    help_test_fix_gregorian_date(sample, expected)


def test_fix_gregorian_date_bst_midnight():
    sample = "2020-10-01T00:00:00.000Z"
    expected = datetime.date(2020, 10, 1)
    help_test_fix_gregorian_date(sample, expected)


def test_fix_gregorian_date_gmt_2300():
    sample = "2020-11-01T23:00:00.000Z"
    expected = datetime.date(2020, 11, 1)
    help_test_fix_gregorian_date(sample, expected)


def help_test_unaware_time_to_utc(sample_time, sample_date, expected,
                                  is_pm=False):
    tz = pytz.timezone('Europe/London')
    h, m = map(int, sample_time.split(':'))
    found = timetable.unaware_time_to_utc(h, m, sample_date, tz, is_pm)
    assert found == expected


def create_utc_datetime(y, m, d, hh, mm):
    return pytz.utc.localize(datetime.datetime(y, m, d, hh, mm))


def test_unaware_time_to_utc_gmt():
    sample_time = "6:01"
    sample_date = datetime.date(2020, 11, 1)
    expected = create_utc_datetime(2020, 11, 1, 6, 1)
    help_test_unaware_time_to_utc(sample_time, sample_date, expected)


def test_unaware_time_to_utc_bst():
    sample_time = "6:01"
    sample_date = datetime.date(2020, 10, 1)
    expected = create_utc_datetime(2020, 10, 1, 5, 1)
    help_test_unaware_time_to_utc(sample_time, sample_date, expected)


def test_unaware_time_to_utc_gmt_pm():
    sample_time = "6:01"
    sample_date = datetime.date(2020, 11, 1)
    expected = create_utc_datetime(2020, 11, 1, 18, 1)
    help_test_unaware_time_to_utc(sample_time, sample_date, expected, True)


def test_is_zuhr_pm():
    prayers_config = config.default_config
    assert timetable.is_ambigious_pm("zuhrbegins", 11, prayers_config) is False
    assert timetable.is_ambigious_pm("zuhrbegins", 1, prayers_config) is True
    assert timetable.is_ambigious_pm("zuhrjamāah", 4, prayers_config) is False


def help_test_auto_am_pm(sample_time, sample_date, prayer, expected):
    found = timetable.unaware_prayer_time_to_utc(sample_time,
                                                 sample_date,
                                                 prayer,
                                                 config.default_config)

    assert found == expected


def test_fajr_am_pm_before_1pm():
    sample_time = "1:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "fajrbegins"
    expected = create_utc_datetime(2020, 11, 1, 1, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_asr_am_pm_after_1pm():
    sample_time = "4:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "asrmithl1"
    expected = create_utc_datetime(2020, 11, 1, 16, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_before_1pm():
    sample_time = "11:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "zuhrbegins"
    expected = create_utc_datetime(2020, 11, 1, 11, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_after_1pm():
    sample_time = "1:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "zuhrbegins"
    expected = create_utc_datetime(2020, 11, 1, 13, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_before_1pm_bst():
    sample_time = "12:59"
    sample_date = datetime.date(2020, 10, 1)
    prayer = "zuhrbegins"
    expected = create_utc_datetime(2020, 10, 1, 11, 59)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_after_1pm_bst():
    sample_time = "1:01"
    sample_date = datetime.date(2020, 10, 1)
    prayer = "zuhrbegins"
    expected = create_utc_datetime(2020, 10, 1, 12, 1)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_new_timetable():
    new_timetable = timetable.create_empty_timetable()

    assert len(new_timetable) == 1
    assert len(new_timetable[tk.DATES]) == 0


def test_get_list_of_date_items(three_unsorted_days):
    built_timetable = timetable.build_timetable(three_unsorted_days,
                                                config.default_config)
    date_dict = built_timetable[tk.DATES]
    assert len(date_dict) == 3
    dt = date_dict[datetime.date(2020, 10, 2)]
    assert dt[tk.ISLAMIC_DATES][tk.TODAY] == (1442, "Safar", 15)
    assert dt[tk.ISLAMIC_DATES][tk.TOMORROW] == (1442, "Safar", 16)


def test_get_sorted_prayer_times(three_unsorted_days):
    prayer = "sunrise"
    prayers_config = config.default_config
    built_timetable = timetable.build_timetable(three_unsorted_days,
                                                prayers_config)

    dates = built_timetable[tk.DATES]
    assert len(dates) == 3

    day = dates[datetime.date(2020, 10, 2)]
    assert len(day) == 2

    times = day[tk.TIMES]
    assert len(times) == len(prayers_config[ck.PRAYERS])
    assert times[prayer] == create_utc_datetime(2020, 10, 2, 6, 0)