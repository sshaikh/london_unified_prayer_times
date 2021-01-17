#!/usr/bin/env python

"""Tests for `london_unified_prayer_times` package."""

import pytest
import json
import jsonschema
import datetime
import pytz

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
    json = lupt.get_json_data(url)
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
    found = lupt.unaware_time_to_utc(sample_time, sample_date, tz, is_pm)
    assert found == expected


def test_unaware_time_to_utc_gmt():
    sample_time = "6:01"
    sample_date = datetime.date(2020, 11, 1)
    expected = pytz.utc.localize(datetime.datetime(2020, 11, 1, 6, 1))
    help_test_unaware_time_to_utc(sample_time, sample_date, expected)


def test_unaware_time_to_utc_bst():
    sample_time = "6:01"
    sample_date = datetime.date(2020, 10, 1)
    expected = pytz.utc.localize(datetime.datetime(2020, 10, 1, 5, 1))
    help_test_unaware_time_to_utc(sample_time, sample_date, expected)


def test_unaware_time_to_utc_gmt_pm():
    sample_time = "6:01"
    sample_date = datetime.date(2020, 11, 1)
    expected = pytz.utc.localize(datetime.datetime(2020, 11, 1, 18, 1))
    help_test_unaware_time_to_utc(sample_time, sample_date, expected, True)


def test_is_zhur_pm():
    assert lupt.is_zhur_pm("11:13") is False
    assert lupt.is_zhur_pm("1:13") is True
    assert lupt.is_zhur_pm("4:13") is False


@pytest.fixture
def pm_prayers():
    prayers = ['asrmithl1', 'asrmithl2', "asrjamāah",
               'maghribbegins', 'maghribjamāah',
               'ishābegins', 'ishājamāah']
    return prayers


@pytest.fixture
def help_test_auto_am_pm(pm_prayers):
    def help_test_auto_am_pm(sample_time, sample_date, prayer, expected):
        found = lupt.unaware_prayer_time_to_utc(sample_time, sample_date,
                                                pytz.timezone('Europe/London'),
                                                prayer, pm_prayers)

        assert found == expected
    return help_test_auto_am_pm


def test_fajr_am_pm_before_1pm(help_test_auto_am_pm):
    sample_time = "1:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "fajrbegins"
    expected = pytz.utc.localize(datetime.datetime(2020, 11, 1, 1, 13))
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_asr_am_pm_after_1pm(help_test_auto_am_pm):
    sample_time = "4:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "asrmithl1"
    expected = pytz.utc.localize(datetime.datetime(2020, 11, 1, 16, 13))
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zhur_am_pm_before_1pm(help_test_auto_am_pm):
    sample_time = "11:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "zuhrbegins"
    expected = pytz.utc.localize(datetime.datetime(2020, 11, 1, 11, 13))
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zhur_am_pm_after_1pm(help_test_auto_am_pm):
    sample_time = "1:13"
    sample_date = datetime.date(2020, 11, 1)
    prayer = "zhurbegins"
    expected = pytz.utc.localize(datetime.datetime(2020, 11, 1, 13, 13))
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zhur_am_pm_before_1pm_bst(help_test_auto_am_pm):
    sample_time = "12:59"
    sample_date = datetime.date(2020, 10, 1)
    prayer = "zuhrbegins"
    expected = pytz.utc.localize(datetime.datetime(2020, 10, 1, 11, 59))
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)


def test_zhur_am_pm_after_1pm_bst(help_test_auto_am_pm):
    sample_time = "1:01"
    sample_date = datetime.date(2020, 10, 1)
    prayer = "zhurbegins"
    expected = pytz.utc.localize(datetime.datetime(2020, 10, 1, 12, 1))
    help_test_auto_am_pm(sample_time, sample_date, prayer, expected)
