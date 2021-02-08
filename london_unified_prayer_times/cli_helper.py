import click
import humanize
import calendar
from datetime import date
from datetime import datetime

from . import constants
from . import cache
from . import query

tk = constants.TimetableKeys
ck = constants.ConfigKeys
clk = constants.ClickKeys


def get_time_format_function(hours, tz):
    def twelve_hours(time):
        return time.astimezone(tz).strftime('%-I:%M %P').rjust(8, ' ')

    def twenty_four_hours(time):
        return time.astimezone(tz).strftime('%H:%M')

    if hours:
        return twelve_hours
    return twenty_four_hours


def load_timetable(ctx):
    def load_timetable():
        name = ctx.obj[clk.NAME]
        return cache.load_cached_timetable(name)
    return load_timetable


def extract_times(ctx, tt):
    passed_times = ctx.obj[clk.USE_TIMES]
    ret = []
    if not passed_times:
        ret = tt[tk.SETUP][tk.CONFIG][ck.DEFAULT_TIMES]
    else:
        available_times = query.get_available_times(tt)
        ret = [x for x in passed_times if x in available_times]
    return ret


def show_day(ctx, requested_date):
    def show_day(tt):
        dt = date.fromisoformat(requested_date)
        day = query.get_day(tt, dt)
        (islamic_y, islamic_m, islamic_d) = day[tk.ISLAMIC_DATES][tk.TODAY]
        click.echo(f'{tt[tk.NAME].capitalize()} timetable for ' +
                   f'{humanize.naturaldate(dt)} ' +
                   f'({islamic_d} {islamic_m} {islamic_y}):\n')
        times = extract_times(ctx, tt)
        format_time = ctx.obj[clk.FORMAT_TIME]
        width = (len(max(times, key=len)) +
                 tt[tk.SETUP][tk.CONFIG][ck.COLUMN_PADDING])
        for time in times:
            raw_time = day[tk.TIMES][time]
            click.echo(f'{time}:'.ljust(width, " ") +
                       f'{format_time(raw_time)}')
    return show_day


def show_calendar(ctx, year, month):
    def show_calendar(tt):
        dt = date(year, month, 1)
        days = query.get_month(tt, dt)
        first_day = next(iter(days.values()))
        (islamic_y, islamic_m, _) = first_day[tk.ISLAMIC_DATES][tk.TODAY]
        click.echo(f'{tt[tk.NAME].capitalize()} timetable for ' +
                   f'{calendar.month_name[month]} {year} ' +
                   f'({islamic_m} {islamic_y}):\n')

        col_padding = tt[tk.SETUP][tk.CONFIG][ck.COLUMN_PADDING]
        num_padding = tt[tk.SETUP][tk.CONFIG][ck.DIGIT_PADDING]
        today_mark = '*'
        times = extract_times(ctx, tt)
        width = len(max(times, key=len)) + col_padding
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
            header = header + f'{time.ljust(width, " ")}'
        click.echo(header)
        format_time = ctx.obj[clk.FORMAT_TIME]
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
            click.echo(line)
    return show_calendar


def humanize_iso(time, when, verb, iso, format_time):
    ret = format_time(time)
    if not iso:
        ret = verb + ' ' + humanize.naturaltime(time, when=when)
    return ret


def now_and_next(ctx, time, iso):
    def now_and_next(tt):
        safe_filter = extract_times(ctx, tt)
        safe_time = (datetime.fromisoformat(time)
                     .astimezone(ctx.obj[clk.TIMEZONE]))
        ret = query.get_now_and_next(tt, safe_filter, safe_time)
        format_time = ctx.obj[clk.FORMAT_TIME]
        if ret[0]:
            humanized = humanize_iso(ret[0][1], safe_time,
                                     'was', iso, format_time)
            click.echo(f'{ret[0][0]} {humanized}')
        if ret[1]:
            humanized = humanize_iso(ret[1][1], safe_time,
                                     'is', iso, format_time)
            click.echo(f'{ret[1][0]} {humanized}')
    return now_and_next
