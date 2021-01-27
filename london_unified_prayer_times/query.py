from . import constants


tk = constants.TimetableKeys


def get_islamic_date(timetable, date, when):
    return timetable[tk.DATES][date][tk.ISLAMIC_DATES][when]


def get_islamic_date_today(timetable, date):
    return get_islamic_date(timetable, date, tk.TODAY)


def get_islamic_date_tomorrow(timetable, date):
    return get_islamic_date(timetable, date, tk.TOMORROW)


def get_available_times(timetable):
    dates = timetable[tk.DATES]

    if len(dates) == 0:
        return []

    day = next(iter(dates.values()))
    return day[tk.TIMES].keys()


def get_time(timetable, date, time):
    return timetable[tk.DATES][date][tk.TIMES][time]
