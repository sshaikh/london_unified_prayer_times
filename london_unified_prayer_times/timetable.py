import dateutil.parser
import pytz
import datetime
from . import constants


tk = constants.TimetableKeys
ck = constants.ConfigKeys


def fix_gregorian_date(from_data, pinfo):
    dt = dateutil.parser.parse(from_data, parserinfo=pinfo)
    return dt.date()


def unaware_time_to_utc(h, m, sample_date, timezone, is_pm=False):
    if is_pm:
        h = h + 12
    time = datetime.time(h, m)
    dt = timezone.localize(datetime.datetime.combine(sample_date, time))
    dt_utc = dt.astimezone(pytz.utc)
    return dt_utc


def is_ambigious_pm(prayer, h, prayers_config):
    return (prayer in prayers_config[ck.AMBIGIOUS_TIMES] and
            (h < prayers_config[ck.AMBIGIOUS_THRESHOLD]))


def prayer_is_pm(prayer, h, prayers_config):
    return (prayer in prayers_config[ck.PM_TIMES] or
            is_ambigious_pm(prayer, h, prayers_config))


def unaware_prayer_time_to_utc(sample_time, sample_date,
                               prayer, prayers_config):
    h, m = map(int, sample_time.split(':'))
    is_pm = prayer_is_pm(prayer, h, prayers_config)
    return unaware_time_to_utc(h, m, sample_date,
                               prayers_config[ck.TIMEZONE], is_pm)


def create_empty_timetable(name, source, config):
    results = {}
    results[tk.NAME] = name
    results[tk.SETUP] = {}
    results[tk.SETUP][tk.SOURCE] = source
    results[tk.SETUP][tk.CONFIG] = config
    results[tk.STATS] = {}
    results[tk.STATS][tk.NUMBER_OF_DATES] = 0
    results[tk.STATS][tk.MIN_DATE] = None
    results[tk.STATS][tk.MAX_DATE] = None
    results[tk.STATS][tk.ISLAMIC_MONTHS] = []
    results[tk.STATS][tk.LAST_UPDATED] = datetime.datetime.utcnow()
    results[tk.DATES] = {}
    return results


def build_timetable(name, source, config, data):
    results = create_empty_timetable(name, source, config)
    dates = results[tk.DATES]
    sorted_data = (sorted(data,
                   key=lambda k: k[config[ck.DATA_GREGORIAN_DATE]]))

    yesterday = None
    islamic_months = set()

    pinfo = dateutil.parser.parserinfo(config[ck.DAY_FIRST],
                                       config[ck.YEAR_FIRST])

    for day in sorted_data:
        dt = fix_gregorian_date(day[config[ck.DATA_GREGORIAN_DATE]], pinfo)

        day_entry = {}
        dates[dt] = day_entry
        islamicdates = {}
        day_entry[tk.ISLAMIC_DATES] = islamicdates

        islamic_month = day[config[ck.DATA_ISLAMIC_MONTH]]
        islamic_months.add(islamic_month)

        today = (int(day[config[ck.DATA_ISLAMIC_YEAR]]),
                 islamic_month,
                 int(day[config[ck.DATA_ISLAMIC_DAY]]))
        islamicdates[tk.TODAY] = today
        if yesterday is not None:
            yesterday[tk.ISLAMIC_DATES][tk.TOMORROW] = today

        prayers = {}

        for prayer in config[ck.TIMES]:
            prayer_time = unaware_prayer_time_to_utc(day[prayer],
                                                     dt, prayer,
                                                     config)
            prayers[prayer] = prayer_time

        day_entry[tk.TIMES] = {k: v for k, v in
                               sorted(prayers.items(), key=lambda k: k[1])}
        yesterday = day_entry

    results[tk.STATS][tk.NUMBER_OF_DATES] = len(dates)
    results[tk.STATS][tk.MIN_DATE] = min(dates.keys())
    results[tk.STATS][tk.MAX_DATE] = max(dates.keys())
    results[tk.STATS][tk.ISLAMIC_MONTHS] = list(islamic_months)

    return results
