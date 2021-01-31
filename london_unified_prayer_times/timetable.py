import dateutil.parser
import pytz
import datetime
from . import constants as c


tk = c.TimetableKeys
ck = c.ConfigKeys


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


def create_empty_timetable(name, source, config, schema):
    results = {}
    date_dict = {}
    results[tk.DATES] = date_dict
    results[tk.SOURCE] = source
    results[tk.NAME] = name
    results[tk.SCHEMA] = schema
    results[tk.CONFIG] = config
    results[tk.NUMBER_OF_DATES] = 0
    return results


def build_timetable(name, source, config, schema, json):
    results = create_empty_timetable(name, source, config, schema)
    dates = results[tk.DATES]

    data = sorted(json[c.JSON_DATA], key=lambda k: k[c.JSON_GREGORIAN_DATE])
    yesterday = None

    for day in data:
        dt = fix_gregorian_date(day[c.JSON_GREGORIAN_DATE],
                                config[ck.TIMEZONE])
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

        for prayer in config[ck.PRAYERS]:
            prayer_time = unaware_prayer_time_to_utc(day[prayer],
                                                     dt, prayer,
                                                     config)
            prayers[prayer] = prayer_time

        yesterday = day_entry

    results[tk.NUMBER_OF_DATES] = len(dates)
    return results
