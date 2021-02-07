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


def get_day(timetable, date):
    return timetable[tk.DATES][date]


def get_month(timetable, date):
    return {k: v for (k, v) in timetable[tk.DATES].items()
            if (k.month == date.month and k.year == date.year)}


def get_now_and_next(timetable, time_filter, query_time):
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

    return ((now_time[1], now_time[0]), (next_time[1], next_time[0]))
