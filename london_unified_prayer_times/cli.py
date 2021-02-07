"""Console script for london_unified_prayer_times."""
import sys
import click
import calendar
from click_default_group import DefaultGroup
from datetime import date
from datetime import datetime
from tzlocal import get_localzone
import pytz
import humanize

from . import cache
from . import config
from . import constants
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


@click.group(cls=DefaultGroup, default='now-and-next', default_if_no_args=True)
@click.option('--timetable', '-t', default=constants.DEFAULT_TIMETABLE,
              help='Name of the local timetable to use')
@click.option('--12h/--24h', 'hours', default=False,
              help='Render times in 24h or 12h')
@click.option('--timezone', '-tz',
              default=get_localzone().zone,
              help='Timezone to render times in')
@click.pass_context
def main(ctx, timetable, hours, timezone):
    """Console script for london_unified_prayer_times."""
    ctx.ensure_object(dict)
    ctx.obj[clk.NAME] = timetable
    tz = pytz.timezone(timezone)
    ctx.obj[clk.TIMEZONE] = tz
    ctx.obj[clk.FORMAT_TIME] = get_time_format_function(hours, tz)
    return 0


def operate_timetable(setup, operate):
    tt = setup()
    if tt:
        operate(tt)
        return 0
    return -1


@main.command()
@click.pass_context
@click.option('--url', '-u', required=True,
              help='URL to retrive timetable from')
@click.option('--config', '-c', 'config_file',
              help='Location of custom config')
@click.option('--schema', '-s', 'schema_file',
              help='Location of custom schema')
def init(ctx, url, config_file, schema_file):
    def setup():
        name = ctx.obj[clk.NAME]
        safe_config = config.load_config(config_file)
        safe_schema = config.load_schema(schema_file)
        return cache.init_timetable(name,
                                    url,
                                    safe_config,
                                    safe_schema)

    def operate(tt):
        click.echo(f'Successfully initialised {tt[tk.NAME]} timetable' +
                   f' with {tt[tk.STATS][tk.NUMBER_OF_DATES]} dates' +
                   f' from {tt[tk.SETUP][tk.SOURCE]}')

    operate_timetable(setup, operate)


@main.command()
@click.pass_context
def refresh(ctx):
    def setup():
        name = ctx.obj[clk.NAME]
        return cache.refresh_timetable_by_name(name)

    def operate(tt):
        click.echo(f'Successfully refreshed {tt[tk.NAME]} timetable' +
                   f' with {tt[tk.STATS][tk.NUMBER_OF_DATES]} dates')

    operate_timetable(setup, operate)


def load_timetable(ctx):
    def load_timetable():
        name = ctx.obj[clk.NAME]
        return cache.load_cached_timetable(name)
    return load_timetable


@main.command(name='list-times')
@click.pass_context
def list_times(ctx):
    def operate(tt):
        click.echo(f'{tt[tk.NAME].capitalize()} timetable ' +
                   'contains times for:\n')
        for time in query.get_available_times(tt):
            click.echo(time)

    operate_timetable(load_timetable(ctx), operate)


@main.command(name='list-dates')
@click.pass_context
def list_dates(ctx):
    def operate(tt):
        click.echo(f'{tt[tk.NAME].capitalize()} timetable contains ' +
                   f'{tt[tk.STATS][tk.NUMBER_OF_DATES]} dates between ' +
                   f'{tt[tk.STATS][tk.MIN_DATE]} and ' +
                   f'{tt[tk.STATS][tk.MAX_DATE]}')

    operate_timetable(load_timetable(ctx), operate)


@main.command(name='show-day')
@click.pass_context
@click.option('--date', '-d', 'requested_date',
              default=date.today().isoformat(),
              help='Date to show times for (defaults to today)')
def show_day(ctx, requested_date):
    def operate(tt):
        dt = date.fromisoformat(requested_date)
        day = query.get_day(tt, dt)
        click.echo(f'{tt[tk.NAME].capitalize()} timetable for ' +
                   f'{dt.isoformat()}:\n')
        format_time = ctx.obj[clk.FORMAT_TIME]
        times = tt[tk.SETUP][tk.CONFIG][ck.TIMES]
        width = len(max(times, key=len)) + 4
        for name, time in day[tk.TIMES].items():
            click.echo(f'{name}:'.ljust(width, " ") +
                       f'{format_time(time)}')

    operate_timetable(load_timetable(ctx), operate)


@main.command(name='show-calendar')
@click.pass_context
@click.option('--year', '-y',
              default=date.today().year,
              help='Year to render calendar for')
@click.option('--month', '-m',
              default=date.today().month,
              help='Month number to render calendar for')
def show_calendar(ctx, year, month):
    def operate(tt):
        dt = date(year, month, 1)
        days = query.get_month(tt, dt)
        first_day = next(iter(days.values()))
        (islamic_y, islamic_m, _) = first_day[tk.ISLAMIC_DATES][tk.TODAY]
        click.echo(f'{tt[tk.NAME].capitalize()} timetable for ' +
                   f'{calendar.month_name[month]} {year} ' +
                   f'({islamic_m} {islamic_y}):\n')

        times = tt[tk.SETUP][tk.CONFIG][ck.TIMES]
        width = len(max(times, key=len)) + 4
        header = 'date'.ljust(8, " ") + 'islamic date'.ljust(24, " ")
        for time in tt[tk.SETUP][tk.CONFIG][ck.TIMES]:
            header = header + f'{time.ljust(width, " ")}'
        click.echo(header)
        format_time = ctx.obj[clk.FORMAT_TIME]
        tday = date.today()
        for k, v in days.items():
            (_, islamic_m, islamic_d) = v[tk.ISLAMIC_DATES][tk.TODAY]
            day_string = str(k.day)
            if k == tday:
                day_string = '*' + day_string.rjust(3, " ")
            line = (f'{day_string.rjust(4, " ")}    '
                    f'{str(islamic_d).rjust(2, " ")} '
                    f'{islamic_m.ljust(21, " ")}')

            ptimes = v[tk.TIMES]
            for time in times:
                line = line + f'{format_time(ptimes[time]).ljust(width, " ")}'
            click.echo(line)

    operate_timetable(load_timetable(ctx), operate)


@main.command(name='now-and-next')
@click.pass_context
@click.option('--time', '-t',
              default=str(datetime.now()),
              help='Current time')
@click.option('--time-filter', '-tf', 'time_filter',
              multiple=True,
              default=[],
              help="Times to consider")
def now_and_next(ctx, time, time_filter):
    def operate(tt):
        safe_filter = list(time_filter)
        safe_time = datetime.fromisoformat(time) \
                            .astimezone(ctx.obj[clk.TIMEZONE])
        if len(time_filter) == 0:
            safe_filter = tt[tk.SETUP][tk.CONFIG][ck.TIMES]
        ret = query.get_now_and_next(tt, safe_filter, safe_time)
        if ret[0]:
            humanized = humanize.naturaltime(ret[0][1], when=safe_time)
            click.echo(f'{ret[0][0]} was {humanized}')
        if ret[1]:
            humanized = humanize.naturaltime(ret[1][1], when=safe_time)
            click.echo(f'{ret[1][0]} is {humanized}')

    operate_timetable(load_timetable(ctx), operate)


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
