import pytest
import json
from london_unified_prayer_times import config
from london_unified_prayer_times import timetable


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
def three_day_timetable(three_unsorted_days):
    prayers_config = config.default_config
    return timetable.build_timetable('pytest',
                                     'conftest.py',
                                     prayers_config,
                                     config.lupt_schema,
                                     three_unsorted_days)


@pytest.fixture
def three_unsorted_days_mock(three_unsorted_days, mocker):
    mocker.patch('london_unified_prayer_times.cache.remote_data.get_json_data',
                 return_value=three_unsorted_days)


@pytest.fixture
def cached_timetable_mock(three_day_timetable, mocker):
    mocker.patch('london_unified_prayer_times.cache.load_cached_timetable',
                 return_value=three_day_timetable)


@pytest.fixture
def refresh_cached_timetable_mock(three_day_timetable, mocker):
    mocker.patch('london_unified_prayer_times.cache.refresh_timetable',
                 return_value=three_day_timetable)


@pytest.fixture
def cache_mock(three_day_timetable, mocker):
    mocker.patch('london_unified_prayer_times.cli.cache.' +
                 'init_timetable',
                 return_value=three_day_timetable)
    mocker.patch('london_unified_prayer_times.cli.cache.' +
                 'refresh_timetable',
                 return_value=three_day_timetable)
    mocker.patch('london_unified_prayer_times.cli.cache.' +
                 'refresh_timetable_by_name',
                 return_value=three_day_timetable)
    mocker.patch('london_unified_prayer_times.cli.cache.' +
                 'load_cached_timetable',
                 return_value=three_day_timetable)
    mocker.patch('london_unified_prayer_times.cli.config.' +
                 'load_config',
                 return_value=config.default_config)
    mocker.patch('london_unified_prayer_times.cli.config.' +
                 'load_schema',
                 return_value=config.lupt_schema)
