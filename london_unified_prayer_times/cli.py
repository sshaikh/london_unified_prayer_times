"""Console script for london_unified_prayer_times."""
import sys
import click
from click_default_group import DefaultGroup
from datetime import date
from datetime import datetime
from tzlocal import get_localzone
import pytz

from . import cache
from . import config
from . import constants
from . import query


tk = constants.TimetableKeys
ck = constants.ConfigKeys
clk = constants.ClickKeys


def get_time_format_function(hours):
    def twelve_hours(time):
        return time.strftime('%-I:%M %P').rjust(8, ' ')
    def twenty_four_hours(time):
        return time.strftime('%H:%M')
    if hours:
        return twelve_hours
    return twenty_four_hours


@click.group(cls=DefaultGroup, default='show-day', default_if_no_args=True)
@click.option('--timetable', '-t', default=constants.PICKLE_FILENAME,
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
    ctx.obj[clk.HOURS] = get_time_format_function(hours)
    ctx.obj[clk.TIMEZONE] = pytz.timezone(timezone)
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
        click.echo(f'{tt[tk.NAME].capitalize()} timetable contains times for:\n')
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
        for name, time in day[tk.TIMES].items():
            local_time = time.astimezone(ctx.obj[clk.TIMEZONE])
            click.echo(f'{name}:\t' +
                       f'{ctx.obj[clk.HOURS](local_time)}')

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
        click.echo(f'{tt[tk.NAME].capitalize()} timetable for ' +
                   f'{year}-{month}:\n')
        header = 'date\tislamic date'
        for time in tt[tk.SETUP][tk.CONFIG][ck.TIMES]:
            header = header + f'\t{time}'
        click.echo(header)
        for k, v in days.items():
            pass


    operate_timetable(load_timetable(ctx), operate)


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
