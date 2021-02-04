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
