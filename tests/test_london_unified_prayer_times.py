#!/usr/bin/env python

"""Tests for `london_unified_prayer_times` package."""

import pytest
import json
import jsonschema
import datetime
import pytz
import appdirs
import os
import shutil
import pickle

from click.testing import CliRunner

from london_unified_prayer_times import london_unified_prayer_times as lupt
from london_unified_prayer_times import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'london_unified_prayer_times.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


@pytest.fixture
def single_day():
    return json.loads("""
    {
        "data": [
            {
                "gregoriandate": "2020-09-30T23:00:00.000Z",
                "islamicday": "14",
                "islamicmonth": "Safar",
                "islamicyear": "1442",
                "sunrise": "6:59",
                "fajrbegins": "5:31",
                "fajrjamāah": "6:01",
                "zuhrbegins": "12:55",
                "zuhrjamāah": "1:30",
                "asrmithl1": "3:55",
                "asrmithl2": "4:43",
                "asrjamāah": "5:00",
                "maghribbegins": "6:40",
                "maghribjamāah": "6:47",
                "ishābegins": "7:58",
                "ishājamāah": "8:15"
            }
        ]
    }
""")


@pytest.fixture
def three_unsorted_days():
    return json.loads("""
    {
        "data": [
            {
                "gregoriandate": "2020-10-02T23:00:00.000Z",
                "islamicday": "16",
                "islamicmonth": "Safar",
                "islamicyear": "1442",
                "sunrise": "7:02",
                "fajrbegins": "5:34",
                "fajrjamāah": "6:04",
                "zuhrbegins": "12:54",
                "zuhrjamāah": "1:30",
                "asrmithl1": "3:52",
                "asrmithl2": "4:39",
                "asrjamāah": "5:00",
                "maghribbegins": "6:36",
                "maghribjamāah": "6:43",
                "ishābegins": "7:55",
                "ishājamāah": "8:15"
            },
            {
                "gregoriandate": "2020-10-01T23:00:00.000Z",
                "islamicday": "15",
                "islamicmonth": "Safar",
                "islamicyear": "1442",
                "sunrise": "7:00",
                "fajrbegins": "5:32",
                "fajrjamāah": "6:02",
                "zuhrbegins": "12:55",
                "zuhrjamāah": "1:45",
                "asrmithl1": "3:54",
                "asrmithl2": "4:41",
                "asrjamāah": "5:00",
                "maghribbegins": "6:38",
                "maghribjamāah": "6:45",
                "ishābegins": "7:56",
                "ishājamāah": "8:15"
            },
            {
                "gregoriandate": "2020-09-30T23:00:00.000Z",
                "islamicday": "14",
                "islamicmonth": "Safar",
                "islamicyear": "1442",
                "sunrise": "6:59",
                "fajrbegins": "5:31",
                "fajrjamāah": "6:01",
                "zuhrbegins": "12:55",
                "zuhrjamāah": "1:30",
                "asrmithl1": "3:55",
                "asrmithl2": "4:43",
                "asrjamāah": "5:00",
                "maghribbegins": "6:40",
                "maghribjamāah": "6:47",
                "ishābegins": "7:58",
                "ishājamāah": "8:15"
            }
        ]
    }
""")


@pytest.fixture
def bad_json():
    return json.loads("""
    {
        "data": [
            {
                "gregosiandate": "2020-09-30T23:00:00.000Z",
                "islamicday": "14",
                "islamicmonth": "Safar",
                "islamicyear": "1442",
                "sunrise": "6:59",
                "fajrbegins": "5:31",
                "fajrjamāah": "6:01",
                "zuhrbegins": "12:55",
                "zuhrjamāah": "1:30",
                "asrmithl1": "3:55",
                "asrmithl2": "4:43",
                "asrjamāah": "5:00",
                "maghribbegins": "6:40",
                "maghribjamāah": "6:47",
                "ishābegins": "7:58",
                "ishājamāah": "8:15"
            }
        ]
    }
""")


@pytest.mark.vcr()
def test_get_json_data():
    url = ("https://mock.location.com/lupt")
    json = lupt.get_json_data(url, lupt.lupt_schema)
    assert json is not None


def test_validate_json(single_day):
    assert jsonschema.validate(single_day, lupt.lupt_schema) is None


def test_invalid_json(bad_json):
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(bad_json, lupt.lupt_schema)


def help_test_fix_gregorian_date(sample_string, expected_date):
    tz = pytz.timezone('Europe/London')
    found = lupt.fix_gregorian_date(sample_string, tz)

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
    found = lupt.unaware_time_to_utc(h, m, sample_date, tz, is_pm)
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


def test_build_config():
    json = lupt.default_config_json
    config = lupt.build_config(json)
    assert len(config) == len(json)
    assert config['timezone'] == pytz.timezone('Europe/London')


def test_is_zuhr_pm():
    prayers_config = lupt.default_config
    assert lupt.is_ambigious_pm("zuhrbegins", 11, prayers_config) is False
    assert lupt.is_ambigious_pm("zuhrbegins", 1, prayers_config) is True
    assert lupt.is_ambigious_pm("zuhrjamāah", 4, prayers_config) is False


@pytest.fixture
def help_test_auto_am_pm():
    def help_test_auto_am_pm(sample_time, sample_date, prayer, expected):
        found = lupt.unaware_prayer_time_to_utc(sample_time, sample_date,
                                                prayer, lupt.default_config)

        assert found == expected
    return help_test_auto_am_pm


def test_fajr_am_pm_before_1pm(help_test_auto_am_pm):
    sample_time = "1:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "fajrbegins"
    expected = create_utc_datetime(2020, 11, 1, 1, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_asr_am_pm_after_1pm(help_test_auto_am_pm):
    sample_time = "4:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "asrmithl1"
    expected = create_utc_datetime(2020, 11, 1, 16, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_before_1pm(help_test_auto_am_pm):
    sample_time = "11:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "zuhrbegins"
    expected = create_utc_datetime(2020, 11, 1, 11, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_after_1pm(help_test_auto_am_pm):
    sample_time = "1:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "zuhrbegins"
    expected = create_utc_datetime(2020, 11, 1, 13, 13)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_before_1pm_bst(help_test_auto_am_pm):
    sample_time = "12:59"
    sample_date = datetime.date(2020, 10, 1)
    prayer = "zuhrbegins"
    expected = create_utc_datetime(2020, 10, 1, 11, 59)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zuhr_am_pm_after_1pm_bst(help_test_auto_am_pm):
    sample_time = "1:01"
    sample_date = datetime.date(2020, 10, 1)
    prayer = "zuhrbegins"
    expected = create_utc_datetime(2020, 10, 1, 12, 1)
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_new_timetable():
    timetable = lupt.create_empty_timetable()

    assert len(timetable) == 1
    assert len(timetable['dates']) == 0


def test_get_list_of_date_items(three_unsorted_days):
    timetable = lupt.build_timetable(three_unsorted_days, lupt.default_config)
    date_dict = timetable['dates']
    assert len(date_dict) == 3
    assert (date_dict[datetime.date(2020, 10, 2)]['islamicdate'] ==
            (1442, "Safar", 15))


def test_get_sorted_prayer_times(three_unsorted_days):
    prayer = "sunrise"
    prayers_config = lupt.default_config
    timetable = lupt.build_timetable(three_unsorted_days, prayers_config)

    dates = timetable['dates']
    assert len(dates) == 3

    day = dates[datetime.date(2020, 10, 2)]
    assert len(day) == 2

    times = day['times']
    assert len(times) == len(prayers_config['prayers'])
    assert times[prayer] == create_utc_datetime(2020, 10, 2, 6, 0)


@pytest.fixture
def timetable(three_unsorted_days):
    prayers_config = lupt.default_config
    return lupt.build_timetable(three_unsorted_days, prayers_config)


def assert_timetable(data, size):
    assert len(data) == 1
    assert len(data['dates']) == size
    day = data['dates'][datetime.date(2020, 10, 2)]
    assert day['islamicdate'] == (1442, "Safar", 15)
    assert (day['times']['sunrise'] ==
            create_utc_datetime(2020, 10, 2, 6, 0))


def test_cache_timetable(timetable):
    appname = "london_unified_prayer_times"
    cache_dir = appdirs.user_cache_dir(appname)
    try:
        shutil.rmtree(cache_dir)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    lupt.cache_timetable(timetable)

    cache_file = cache_dir + '/timetable.pickle'
    with open(cache_file, 'rb') as cache_json:
        data = pickle.load(cache_json)

        assert_timetable(data, 3)

        try:
            os.remove(cache_file)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


def test_read_cached_timetable(timetable):
    lupt.cache_timetable(timetable)
    data = lupt.load_cached_timetable()

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
    data = lupt.refresh_timetable(url,
                                  lupt.lupt_schema,
                                  lupt.default_config)
    assert_timetable(data, 457)


# def test_get_next_prayer_time():
