import pytest
import dateutil.parser
from london_unified_prayer_times import config
from london_unified_prayer_times import timetable


@pytest.fixture
def single_day():
    return [
                {'Gregorian date': '01/10/2021',
                 'Islamic day': '24',
                 'Islamic month': 'Safar',
                 'Islamic year': '1443',
                 'Sunrise': '6:58',
                 'Fajr Begins': '5:30',
                 "Fajr Jamā'ah": '5:50',
                 'Zuhr Begins': '12:55',
                 "Zuhr Jamā'ah": '1:45',
                 'Asr Mithl 1': '3:56',
                 'Asr Mithl 2': '4:43',
                 "Asr Jamā'ah": '5:00',
                 'Maghrib Begins': '6:41',
                 "Maghrib Jamā'ah": '6:48',
                 'Ishā Begins': '7:59',
                 "Ishā Jamā'ah": '8:15'}
           ]


@pytest.fixture
def bad_parse():
    return [
                {'Gregorin date': '01/10/2021',
                 'Islamic day': '24',
                 'Islamic month': 'Safar',
                 'Islamic year': '1443',
                 'Sunrise': '6:58',
                 'Fajr Begins': '5:30',
                 "Fajr Jamā'ah": '5:50',
                 'Zuhr Begins': '12:55',
                 "Zuhr Jamā'ah": '1:45',
                 'Asr Mithl 1': '3:56',
                 'Asr Mithl 2': '4:43',
                 "Asr Jamā'ah": '5:00',
                 'Maghrib Begins': '6:41',
                 "Maghrib Jamā'ah": '6:48',
                 'Ishā Begins': '7:59',
                 "Ishā Jamā'ah": '8:15'}
           ]


@pytest.fixture
def three_unsorted_days():
    return [
                {'Gregorian date': '03/10/2021',
                 'Islamic day': '26',
                 'Islamic month': 'Safar',
                 'Islamic year': '1443',
                 'Sunrise': '7:02',
                 'Fajr Begins': '5:34',
                 "Fajr Jamā'ah": '5:54',
                 'Zuhr Begins': '12:54',
                 "Zuhr Jamā'ah": '1:30',
                 'Asr Mithl 1': '3:53',
                 'Asr Mithl 2': '4:39',
                 "Asr Jamā'ah": '5:00',
                 'Maghrib Begins': '6:36',
                 "Maghrib Jamā'ah": '6:43',
                 'Ishā Begins': '7:55',
                 "Ishā Jamā'ah": '8:15'},
                {'Gregorian date': '02/10/2021',
                 'Islamic day': '25',
                 'Islamic month': 'Safar',
                 'Islamic year': '1443',
                 'Sunrise': '7:00',
                 'Fajr Begins': '5:32',
                 "Fajr Jamā'ah": '5:52',
                 'Zuhr Begins': '12:55',
                 "Zuhr Jamā'ah": '1:30',
                 'Asr Mithl 1': '3:54',
                 'Asr Mithl 2': '4:41',
                 "Asr Jamā'ah": '5:00',
                 'Maghrib Begins': '6:39',
                 "Maghrib Jamā'ah": '6:46',
                 'Ishā Begins': '7:57',
                 "Ishā Jamā'ah": '8:15'},
                {'Gregorian date': '01/10/2021',
                 'Islamic day': '24',
                 'Islamic month': 'Safar',
                 'Islamic year': '1443',
                 'Sunrise': '6:58',
                 'Fajr Begins': '5:30',
                 "Fajr Jamā'ah": '5:50',
                 'Zuhr Begins': '12:55',
                 "Zuhr Jamā'ah": '1:45',
                 'Asr Mithl 1': '3:56',
                 'Asr Mithl 2': '4:43',
                 "Asr Jamā'ah": '5:00',
                 'Maghrib Begins': '6:41',
                 "Maghrib Jamā'ah": '6:48',
                 'Ishā Begins': '7:59',
                 "Ishā Jamā'ah": '8:15'}
                   ]


@pytest.fixture
def parserinfo():
    return dateutil.parser.parserinfo(True, False)


@pytest.fixture
def three_day_timetable(three_unsorted_days):
    prayers_config = config.default_config
    return timetable.build_timetable('pytest',
                                     'conftest.py',
                                     prayers_config,
                                     three_unsorted_days)


@pytest.fixture
def three_unsorted_days_mock(three_unsorted_days, mocker):
    mocker.patch('london_unified_prayer_times.cache.remote_data.get_html_data',
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
