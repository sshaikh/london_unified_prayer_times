#!/usr/bin/env python

"""Tests for `london_unified_prayer_times` package."""

import pytest
import json
import jsonschema
import datetime

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


@pytest.fixture
def london_timezone():
    return 'Europe/London'


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


def test_fix_gregorian_date_bst(london_timezone):
    sample = "2020-10-01T23:00:00.000Z"
    expected = datetime.date(2020, 10, 2)
    found = lupt.fix_gregorian_date(sample, london_timezone)

    assert found == expected


def test_fix_gregorian_date_gmt(london_timezone):
    sample = "2020-11-01T00:00:00.000Z"
    expected = datetime.date(2020, 11, 1)
    found = lupt.fix_gregorian_date(sample, london_timezone)

    assert found == expected


def test_fix_gregorian_date_bst_midnight(london_timezone):
    sample = "2020-10-01T00:00:00.000Z"
    expected = datetime.date(2020, 10, 1)
    found = lupt.fix_gregorian_date(sample, london_timezone)

    assert found == expected


def test_fix_gregorian_date_gmt_2300(london_timezone):
    sample = "2020-11-01T23:00:00.000Z"
    expected = datetime.date(2020, 11, 1)
    found = lupt.fix_gregorian_date(sample, london_timezone)

    assert found == expected
