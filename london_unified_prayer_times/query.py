from bisect import bisect
from datetime import timedelta

from . import constants


tk = constants.TimetableKeys
ck = constants.ConfigKeys


def get_islamic_date(timetable, date, when):
    return timetable[tk.DATES][date][tk.ISLAMIC_DATES][when]


def get_islamic_date_today(timetable, date):
    return get_islamic_date(timetable, date, tk.TODAY)


def get_islamic_date_tomorrow(timetable, date):
    return get_islamic_date(timetable, date, tk.TOMORROW)


def get_available_times(timetable):
    return timetable[tk.SETUP][tk.CONFIG][ck.TIMES]


def get_time(timetable, date, time):
    return timetable[tk.DATES][date][tk.TIMES][time]


def extract_times(tt, use_times):
    ret = use_times

    if not ret:
        ret = tt[tk.SETUP][tk.CONFIG][ck.DEFAULT_TIMES]

    available_times = get_available_times(tt)
    ret = [x for x in ret if x in available_times]
    return ret


def get_day(timetable, date, use_times):
    times = extract_times(timetable, use_times)
    ret = []
    day = timetable[tk.DATES][date][tk.TIMES]
    for time in times:
        ret.append((time, day[time]))

    return ret


def get_month(timetable, year, month, use_times):
    times = extract_times(timetable, use_times)
    header = ('Date', 'Islamic Date', times)

    days = [(dt, tms[tk.ISLAMIC_DATES][tk.TODAY],
             [tms[tk.TIMES][tm] for tm in times])
            for dt, tms in timetable[tk.DATES].items()
            if dt.month == month and dt.year == year]

    return (header, days)


def get_info(timetable):
    return (timetable[tk.NAME],
            timetable[tk.SETUP][tk.SOURCE],
            (timetable[tk.STATS][tk.NUMBER_OF_DATES],
             timetable[tk.STATS][tk.MIN_DATE],
             timetable[tk.STATS][tk.MAX_DATE]),
            (timetable[tk.STATS][tk.LAST_UPDATED],
             timetable[tk.SETUP][tk.CONFIG][ck.CACHE_EXPIRY]))


def get_config(timetable):
    return timetable[tk.SETUP][tk.CONFIG]


def get_now_and_next(timetable, time_filter, query_time):
    time_filter = extract_times(timetable, time_filter)
    dt = query_time.date()
    ordered_times = []
    dates = timetable[tk.DATES]
    times = dates[dt][tk.TIMES]
    # let's do it this way as timetable times are sorted
    for k, v in times.items():
        if k in time_filter:
            ordered_times.append((v, k))

    index = bisect(ordered_times, (query_time, 'zzzzzzz'))

    now_time = None
    next_time = None

    if index == 0:
        next_time = ordered_times[index]
        yesterday_date = dt - timedelta(days=1)
        if yesterday_date in dates:
            yesterday_times = dates[yesterday_date][tk.TIMES]
            items = list(yesterday_times.items())
            items.reverse()
            for item in items:
                if item[0] in time_filter:
                    now_time = (item[1], item[0])
                    break
    elif index == len(ordered_times):
        now_time = ordered_times[index-1]
        tomorrow_date = dt + timedelta(days=1)
        if tomorrow_date in dates:
            tomorrow_times = dates[tomorrow_date][tk.TIMES]
            for item in tomorrow_times.items():
                if item[0] in time_filter:
                    next_time = (item[1], item[0])
                    break
    else:
        now_time = ordered_times[index - 1]
        next_time = ordered_times[index]

    return ((now_time[1], now_time[0]),
            (next_time[1], next_time[0]))
