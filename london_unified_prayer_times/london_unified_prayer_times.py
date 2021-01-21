"""Main module."""

import urllib.request
import json
import jsonschema
import importlib.resources as pkg_resources
import dateutil.parser
import pytz
import datetime
import os
import appdirs
import pickle
from london_unified_prayer_times import constants as c


tk = c.TimetableKeys
ck = c.ConfigKeys


def build_config(json):
    config = {}
    for k in ck:
        config[k] = json[k.value]
    config[ck.TIMEZONE] = pytz.timezone(json[ck.TIMEZONE.value])
    return config


def get_json_data(url, schema):
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
    return (prayer in prayers_config[ck.AMBIGIOUS_PRAYERS] and
            (h < prayers_config[ck.AMBIGIOUS_THRESHOLD]))


def prayer_is_pm(prayer, h, prayers_config):
    return (prayer in prayers_config[ck.PM_PRAYERS] or
            is_ambigious_pm(prayer, h, prayers_config))


def unaware_prayer_time_to_utc(sample_time, sample_date,
                               prayer, prayers_config):
    h, m = map(int, sample_time.split(':'))
    is_pm = prayer_is_pm(prayer, h, prayers_config)
    return unaware_time_to_utc(h, m, sample_date,
                               prayers_config[ck.TIMEZONE], is_pm)


def create_empty_timetable():
    results = {}
    date_dict = {}
    results[tk.DATES] = date_dict
    return results


def build_timetable(json, prayers_config):
    results = create_empty_timetable()
    dates = results[tk.DATES]

    data = sorted(json[c.JSON_DATA], key=lambda k: k[c.JSON_GREGORIAN_DATE])
    yesterday = None

    for day in data:
        dt = fix_gregorian_date(day[c.JSON_GREGORIAN_DATE],
                                prayers_config[ck.TIMEZONE])
        day_entry = {}
        dates[dt] = day_entry
        islamicdates = {}
        day_entry[tk.ISLAMIC_DATES] = islamicdates

        today = (int(day[c.JSON_ISLAMIC_YEAR]),
                 day[c.JSON_ISLAMIC_MONTH],
                 int(day[c.JSON_ISLAMIC_DAY]))
        islamicdates[tk.TODAY] = today
        if yesterday is not None:
            yesterday[tk.ISLAMIC_DATES][tk.TOMORROW] = today

        prayers = {}
        day_entry[tk.TIMES] = prayers

        for prayer in prayers_config[ck.PRAYERS]:
            prayer_time = unaware_prayer_time_to_utc(day[prayer],
                                                     dt, prayer,
                                                     prayers_config)
            prayers[prayer] = prayer_time

        yesterday = day_entry

    return results


def get_cache_fileinfo():
    cache_dir = appdirs.user_cache_dir(__package__)
    cache_file = cache_dir + '/' + c.PICKLE_FILENAME
    return cache_dir, cache_file


def cache_timetable(timetable):
    cache_dir, cache_file = get_cache_fileinfo()

    os.makedirs(cache_dir, exist_ok=True)
    try:
        os.remove(cache_file)
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    with open(cache_file, 'wb') as outfile:
        pickle.dump(timetable, outfile)


def load_cached_timetable():
    cache_dir, cache_file = get_cache_fileinfo()

    with open(cache_file, 'rb') as cached_pickle:
        return pickle.load(cached_pickle)


def refresh_timetable(url, schema, config):
    json = get_json_data(url, schema)
    timetable = build_timetable(json, config)
    cache_timetable(timetable)
    return timetable


lupt_schema = json.loads(pkg_resources.read_text(__package__, 'schema.json'))
default_config_json = json.loads(
    pkg_resources.read_text(__package__, 'default_config.json'))
default_config = build_config(default_config_json)
