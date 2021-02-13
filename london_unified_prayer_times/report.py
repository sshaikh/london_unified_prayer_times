import json
import humanize
import calendar
from datetime import date

from . import constants as c
from . import query

tk = c.TimetableKeys
ck = c.ConfigKeys


def get_time_format_function(hours, tz):
    def twelve_hours(time):
        return time.astimezone(tz).strftime('%-I:%M %P').rjust(8, ' ')

    def twenty_four_hours(time):
        return time.astimezone(tz).strftime('%H:%M')

    if hours:
        return twelve_hours
    return twenty_four_hours


def extract_replace_strings(tt, replace_strings):
    ret = replace_strings
    if not ret:
        ret = tt[tk.SETUP][tk.CONFIG][ck.DEFAULT_REPLACE_STRINGS]
    return ret


def generate_heading(heading):
    return f'=== {heading} ===\n\n'


def show_info(tt):
    info = query.get_info(tt)

    ret = generate_heading(f'{info[0].capitalize()} timetable')

    ret += f'Downloaded from {info[1]}\n\n'
    cache_expiry = info[3][1]
    cache_string = humanize.naturaldelta(cache_expiry)
    ret += f'Last updated on {info[3][0]}\n'
    ret += f'Default cache expiry set to {cache_string}\n\n'

    ret += (f'{info[2][0]} dates available between '
            f'{info[2][1]} and '
            f'{info[2][2]} with the following times:\n\n')

    for time in query.get_available_times(tt):
        ret += time + '\n'

    config = query.get_config(tt)
    ret += '\nConfig:\n\n'
    ret += str(config[0])

    ret += '\nSchema:\n\n'
    ret += json.dumps(config[1]) + '\n'
    return ret


def perform_replace_strings(string, replace_strings):
    ret = string
    for (s, g) in replace_strings:
        ret = ret.replace(s, g)
    return ret


def calculate_time_width(times, rs, padding):
    replaced = []
    for time in times:
        replaced.append(perform_replace_strings(time, rs))
    return len(max(replaced, key=len)) + padding


def calculate_time_width_tuple(times, padding):
    return len(max(times, key=len)) + padding


def show_day(tt, dt, use_times, replace_strings, hours, tz):
    rs = extract_replace_strings(tt, replace_strings)
    format_time = get_time_format_function(hours, tz)
    day = query.get_day(tt, dt, use_times)

    replaced_day = [(perform_replace_strings(time, rs), raw_time)
                    for time, raw_time in day]

    (islamic_y, islamic_m, islamic_d) = query.get_islamic_date_today(tt, dt)
    info = query.get_info(tt)
    ret = (f'{info[0].capitalize()} timetable for '
           f'{humanize.naturaldate(dt)} '
           f'({islamic_d} {islamic_m} {islamic_y}):\n\n')
    times = [time for time, _ in replaced_day]
    width = calculate_time_width_tuple(times, c.COLUMN_PADDING)
    for time, raw_time in replaced_day:
        ret += f'{time}:'.ljust(width, " ")
        ret += f'{format_time(raw_time)}\n'
    return ret


def show_calendar(tt, year, month, use_times, replace_strings, hours, tz):
    times = query.extract_times(tt, use_times)
    rs = extract_replace_strings(tt, replace_strings)
    format_time = get_time_format_function(hours, tz)
    dt = date(year, month, 1)
    days = query.get_month(tt, dt)
    first_day = next(iter(days.values()))
    (islamic_y, islamic_m, _) = first_day[tk.ISLAMIC_DATES][tk.TODAY]
    ret = (f'{tt[tk.NAME].capitalize()} timetable for '
           f'{calendar.month_name[month]} {year} '
           f'({islamic_m} {islamic_y}):\n\n')

    col_padding = c.COLUMN_PADDING
    num_padding = c.DIGIT_PADDING
    today_mark = '*'
    clock_width = 8 if hours else 5
    width = max(calculate_time_width(times, rs, col_padding),
                clock_width + col_padding)
    header_date = 'date'
    dt_width = (max(len(header_date),
                    num_padding + len(today_mark) + 1)
                + col_padding)
    header_islamic_date = 'islamic date'
    islamic_months = set()
    for day in days.values():
        islamic_months.add(day[tk.ISLAMIC_DATES][tk.TODAY][1])
    max_month = len(max(islamic_months, key=len))
    im_width = (max(len(header_islamic_date), max_month) +
                num_padding + 1 + col_padding)
    header = (str(header_date.ljust(dt_width, " ")) +
              str(header_islamic_date.ljust(im_width, " ")))

    for time in times:
        header += f'{perform_replace_strings(time, rs).ljust(width, " ")}'
    ret += header + '\n'
    tday = date.today()
    for k, v in days.items():
        (_, islamic_m, islamic_d) = v[tk.ISLAMIC_DATES][tk.TODAY]
        day_string = str(k.day)
        if k == tday:
            day_string = (today_mark + ' ' +
                          day_string.rjust(num_padding, " "))
        line = (f'{day_string.rjust(col_padding, " ")}    '
                f'{str(islamic_d).rjust(num_padding, " ")} '
                f'{islamic_m.ljust(im_width - num_padding - 1, " ")}')

        ptimes = v[tk.TIMES]
        for time in times:
            line = line + f'{format_time(ptimes[time]).ljust(width, " ")}'
        ret += line + '\n'
    return ret


def humanize_iso(time, when, verb, iso, format_time):
    ret = format_time(time)
    if not iso:
        ret = verb + ' ' + humanize.naturaltime(time, when=when)
    return ret


def now_and_next(tt, time, iso, use_times, replace_strings, hours, tz):
    times = query.extract_times(tt, use_times)
    ret = query.get_now_and_next(tt, times, time)
    format_time = get_time_format_function(hours, tz)
    rs = extract_replace_strings(tt, replace_strings)
    ret_str = ""
    if ret[0]:
        humanized = humanize_iso(ret[0][1], time,
                                 'was', iso, format_time)
        ret_str += f'{perform_replace_strings(ret[0][0], rs)} {humanized}\n'
    if ret[1]:
        humanized = humanize_iso(ret[1][1], time,
                                 'is', iso, format_time)
        ret_str += f'{perform_replace_strings(ret[1][0], rs)} {humanized}\n'
    return ret_str