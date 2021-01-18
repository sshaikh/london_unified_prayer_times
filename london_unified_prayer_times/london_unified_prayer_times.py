"""Main module."""

import urllib.request
import json
import jsonschema
import importlib.resources as pkg_resources
import dateutil.parser
import pytz
import datetime


lupt_schema = json.loads(pkg_resources.read_text(__package__, 'schema.json'))


def get_json_data(url, schema=lupt_schema):
    with urllib.request.urlopen(url) as data:
        json_data = json.loads(data.read().decode())
        jsonschema.validate(json_data, schema)
        return json_data


def fix_gregorian_date(from_json, timezone):
    dt = dateutil.parser.parse(from_json)
    dt = dt.astimezone(timezone)
    return dt.date()


def unaware_time_to_utc(h, m, sample_date, timezone, is_pm=False):
    if is_pm:
        h = h + 12
    time = datetime.time(h, m)
    dt = timezone.localize(datetime.datetime.combine(sample_date, time))
    dt_utc = dt.astimezone(pytz.utc)
    return dt_utc


def is_ambigious_pm(prayer, h, prayers_config):
    return (prayer in prayers_config['ambigious_prayers'] and
            (h < prayers_config['ambigious_threshold']))


def prayer_is_pm(prayer, h, prayers_config):
    return (prayer in prayers_config['pm_prayers'] or
            is_ambigious_pm(prayer, h, prayers_config))


def unaware_prayer_time_to_utc(sample_time, sample_date,
                               prayer, prayers_config):
    h, m = map(int, sample_time.split(':'))
    is_pm = prayer_is_pm(prayer, h, prayers_config)
    return unaware_time_to_utc(h, m, sample_date,
                               prayers_config['timezone'], is_pm)


def create_empty_timetable(prayer_list):
    results = {}
    prayers = {}

    for prayer in prayer_list:
        prayers[prayer] = []

    results['prayer_times'] = prayers

    date_dict = {}
    results['dates'] = date_dict
    return results


def build_timetable(json, prayers_config):
    results = create_empty_timetable(prayers_config['prayers'])
    prayers = results['prayer_times']
    dates = results['dates']

    data = sorted(json['data'], key=lambda k: k['gregoriandate'])

    for day in data:
        dt = fix_gregorian_date(day['gregoriandate'],
                                prayers_config['timezone'])
        dates[dt] = (int(day['islamicyear']),
                     day['islamicmonth'],
                     int(day['islamicday']))
        for prayer in prayers_config['prayers']:
            prayer_time = unaware_prayer_time_to_utc(day[prayer],
                                                     dt, prayer,
                                                     prayers_config)
            prayers[prayer].append(prayer_time)

    return results
