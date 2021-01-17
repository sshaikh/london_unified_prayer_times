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


def is_zhur_pm(h, threshold):
    return (h < threshold)


def unaware_prayer_time_to_utc(sample_time, sample_date, timezone,
                               prayer, pm_prayers, zhur_threshold):
    h, m = map(int, sample_time.split(':'))
    is_pm = ((prayer in pm_prayers) or
             (prayer.startswith("zhur") and is_zhur_pm(h, zhur_threshold)))
    return unaware_time_to_utc(h, m, sample_date, timezone, is_pm)
