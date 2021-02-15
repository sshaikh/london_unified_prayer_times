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
    info = query.get_info(tt)

    (islamic_y, islamic_m, islamic_d) = query.get_islamic_date_today(tt, dt)
    ret = (f'{info[0].capitalize()} timetable for '
           f'{humanize.naturaldate(dt)} '
           f'({islamic_d} {islamic_m} {islamic_y}):\n\n')

    formatted_day = [(perform_replace_strings(time, rs),
                     format_time(raw_time))
                     for time, raw_time in day]

    times = [time for time, _ in formatted_day]
    width = calculate_time_width_tuple(times, c.COLUMN_PADDING)

    for time, raw_time in formatted_day:
        ret += f'{time}:'.ljust(width, " ")
        ret += f'{raw_time}\n'

    return ret


def show_calendar(tt, year, month, use_times, replace_strings, hours, tz):
    rs = extract_replace_strings(tt, replace_strings)
    format_time = get_time_format_function(hours, tz)

    info = query.get_info(tt)
    (header, days) = query.get_month(tt, year, month, use_times)

    dt = date(year, month, 1)
    (islamic_y, islamic_m, _) = query.get_islamic_date_today(tt, dt)
    (fdt, (islamic_y, islamic_m, _), _) = next(iter(days))

    ret = (f'{info[0].capitalize()} timetable for '
           f'{calendar.month_name[fdt.month]} {fdt.year} '
           f'({islamic_m} {islamic_y}):\n\n')

    formatted_header = ((header[0], header[1]) +
                        tuple(perform_replace_strings(col, rs)
                              for col in header[2]))

    formatted_days = [formatted_header]
    tday = date.today()
    today_mark = '*'
    for day in days:
        day_string = str(day[0].day).rjust(2, " ")
        if day[0] == tday:
            day_string = f'{today_mark} {day_string}'
        day_string = day_string.rjust(4, " ")
        iday_string = f'{str(day[1][2]).rjust(2, " ")} {day[1][1]}'
        day_tuple = ((day_string, iday_string) +
                     tuple(format_time(t) for t in day[2]))
        formatted_days.append(day_tuple)

    col_padding = c.COLUMN_PADDING
    dt_header_width = max(len(item[0])
                          for item in formatted_days) + col_padding
    idt_header_width = max(len(item[1])
                           for item in formatted_days) + col_padding
    time_header_width = max(max(len(tm) for tm in day[2:])
                            for day in formatted_days) + col_padding

    for line in formatted_days:
        ret += line[0].ljust(dt_header_width, " ")
        ret += line[1].ljust(idt_header_width, " ")
        for tm in line[2:]:
            ret += tm.ljust(time_header_width, " ")
        ret += '\n'

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
