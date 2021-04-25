from freezegun import freeze_time
import datetime
import pytz
from london_unified_prayer_times import config
from london_unified_prayer_times import timetable
from london_unified_prayer_times import constants


tk = constants.TimetableKeys
ck = constants.ConfigKeys


def help_test_fix_gregorian_date(sample_string, expected_date, pinfo):
    found = timetable.fix_gregorian_date(sample_string, pinfo)

    assert found == expected_date


def test_fix_gregorian_date(parserinfo):
    sample = "01/10/2021"
    expected = datetime.date(2021, 10, 1)
    help_test_fix_gregorian_date(sample, expected, parserinfo)


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
    sample_date = datetime.date(2021, 11, 1)
    expected = create_utc_datetime(2021, 11, 1, 6, 1)
    help_test_unaware_time_to_utc(sample_time, sample_date, expected)


def test_unaware_time_to_utc_bst():
    sample_time = "6:01"
    sample_date = datetime.date(2021, 10, 1)
    expected = create_utc_datetime(2021, 10, 1, 5, 1)
    help_test_unaware_time_to_utc(sample_time, sample_date, expected)


def test_unaware_time_to_utc_gmt_pm():
    sample_time = "6:01"
    sample_date = datetime.date(2021, 11, 1)
    expected = create_utc_datetime(2021, 11, 1, 18, 1)
    help_test_unaware_time_to_utc(sample_time, sample_date, expected, True)


def test_is_zuhr_pm():
    prayers_config = config.default_config
    assert (timetable.is_ambigious_pm("Zuhr Begins", 11, prayers_config)
            is False)
    assert timetable.is_ambigious_pm("Zuhr Begins", 1, prayers_config) is True
    assert (timetable.is_ambigious_pm("Zuhr Jamā'ah", 4, prayers_config)
            is False)


def help_test_auto_am_pm(sample_time, sample_date, prayer, expected):
    found = timetable.unaware_prayer_time_to_utc(sample_time,
                                                 sample_date,
                                                 prayer,
                                                 config.default_config)

    assert found == expected


def test_fajr_am_pm_before_1pm():
    sample_time = "1:13"
    sample_date = datetime.date(2021, 11, 1)
    prayer = "Fajr Begins"
    expected = create_utc_datetime(2021, 11, 1, 1, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_asr_am_pm_after_1pm():
    sample_time = "4:13"
    sample_date = datetime.date(2021, 11, 1)
    prayer = "Asr Mithl 1"
    expected = create_utc_datetime(2021, 11, 1, 16, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_before_1pm():
    sample_time = "11:13"
    sample_date = datetime.date(2021, 11, 1)
    prayer = "Zuhr Begins"
    expected = create_utc_datetime(2021, 11, 1, 11, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_after_1pm():
    sample_time = "1:13"
    sample_date = datetime.date(2021, 11, 1)
    prayer = "Zuhr Begins"
    expected = create_utc_datetime(2021, 11, 1, 13, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_before_1pm_bst():
    sample_time = "12:59"
    sample_date = datetime.date(2021, 10, 1)
    prayer = "Zuhr Begins"
    expected = create_utc_datetime(2021, 10, 1, 11, 59)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_after_1pm_bst():
    sample_time = "1:01"
    sample_date = datetime.date(2021, 10, 1)
    prayer = "Zuhr Begins"
    expected = create_utc_datetime(2021, 10, 1, 12, 1)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


@freeze_time("2020-10-15 15:15:15")
def test_new_timetable():
    name = 'test_timetable'
    source = 'test_source'
    dconfig = config.default_config

    new_timetable = timetable.create_empty_timetable(name,
                                                     source,
                                                     dconfig)

    assert len(new_timetable[tk.DATES]) == 0
    assert new_timetable[tk.STATS][tk.NUMBER_OF_DATES] == 0
    assert new_timetable[tk.STATS][tk.MIN_DATE] is None
    assert new_timetable[tk.STATS][tk.MAX_DATE] is None
    assert len(new_timetable[tk.STATS][tk.ISLAMIC_MONTHS]) == 0
    assert new_timetable[tk.SETUP][tk.SOURCE] is source
    assert new_timetable[tk.NAME] is name
    assert new_timetable[tk.SETUP][tk.CONFIG] is dconfig
    assert (new_timetable[tk.STATS][tk.LAST_UPDATED] ==
            datetime.datetime.fromisoformat("2020-10-15 15:15:15"))


def test_get_list_of_date_items(three_day_timetable):
    date_dict = three_day_timetable[tk.DATES]
    assert three_day_timetable[tk.STATS][tk.NUMBER_OF_DATES] == len(date_dict)
    dt = date_dict[datetime.date(2021, 10, 2)]
    assert dt[tk.ISLAMIC_DATES][tk.TODAY] == (1443, "Safar", 25)
    assert dt[tk.ISLAMIC_DATES][tk.TOMORROW] == (1443, "Safar", 26)


def test_get_sorted_prayer_times(three_day_timetable):
    prayer = "Sunrise"
    prayers_config = config.default_config

    dates = three_day_timetable[tk.DATES]

    day = dates[datetime.date(2021, 10, 2)]
    assert len(day) == 2

    times = day[tk.TIMES]
    assert len(times) == len(prayers_config[ck.TIMES])
    assert times[prayer] == create_utc_datetime(2021, 10, 2, 6, 0)

    assert three_day_timetable[tk.NAME] == 'pytest'
    assert three_day_timetable[tk.SETUP][tk.CONFIG] == prayers_config


def test_min_max_dates(three_day_timetable):
    assert (three_day_timetable[tk.STATS][tk.MIN_DATE] ==
            datetime.date(2021, 10, 1))
    assert (three_day_timetable[tk.STATS][tk.MAX_DATE] ==
            datetime.date(2021, 10, 3))


def test_months(three_day_timetable):
    assert len(three_day_timetable[tk.STATS][tk.ISLAMIC_MONTHS]) == 1
