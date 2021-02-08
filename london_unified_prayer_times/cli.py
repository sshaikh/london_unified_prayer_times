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
from . import cli_helper


tk = constants.TimetableKeys
ck = constants.ConfigKeys
clk = constants.ClickKeys


@click.group(cls=DefaultGroup, default='now-and-next', default_if_no_args=True)
@click.option('--timetable', '-t', default=constants.DEFAULT_TIMETABLE,
              help='Name of the local timetable to use')
@click.option('--12h/--24h', 'hours', default=False,
              help='Render times in 24h or 12h')
@click.option('--timezone', '-tz',
              default=get_localzone().zone,
              help='Timezone to render times in')
@click.option('--use-time', '-ut', 'time_filter',
              multiple=True,
              default=[],
              help="Times to consider")
@click.pass_context
def main(ctx, timetable, hours, timezone, time_filter):
    """Console script for london_unified_prayer_times."""
    ctx.ensure_object(dict)
    ctx.obj[clk.NAME] = timetable
    tz = pytz.timezone(timezone)
    ctx.obj[clk.TIMEZONE] = tz
    ctx.obj[clk.FORMAT_TIME] = cli_helper.get_time_format_function(hours, tz)
    ctx.obj[clk.USE_TIMES] = time_filter
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


@main.command(name='list-times')
@click.pass_context
def list_times(ctx):
    def operate(tt):
        click.echo(f'{tt[tk.NAME].capitalize()} timetable ' +
                   'contains times for:\n')
        for time in query.get_available_times(tt):
            click.echo(time)

    operate_timetable(cli_helper.load_timetable(ctx), operate)


@main.command(name='list-dates')
@click.pass_context
def list_dates(ctx):
    def operate(tt):
        click.echo(f'{tt[tk.NAME].capitalize()} timetable contains ' +
                   f'{tt[tk.STATS][tk.NUMBER_OF_DATES]} dates between ' +
                   f'{tt[tk.STATS][tk.MIN_DATE]} and ' +
                   f'{tt[tk.STATS][tk.MAX_DATE]}')

    operate_timetable(cli_helper.load_timetable(ctx), operate)


@main.command(name='show-day')
@click.pass_context
@click.option('--date', '-d', 'requested_date',
              default=date.today().isoformat(),
              help='Date to show times for (defaults to today)')
def show_day(ctx, requested_date):
    operate_timetable(cli_helper.load_timetable(ctx),
                      cli_helper.show_day(ctx, requested_date))


@main.command(name='show-calendar')
@click.pass_context
@click.option('--year', '-y',
              default=date.today().year,
              help='Year to render calendar for')
@click.option('--month', '-m',
              default=date.today().month,
              help='Month number to render calendar for')
def show_calendar(ctx, year, month):
    operate_timetable(cli_helper.load_timetable(ctx),
                      cli_helper.show_calendar(ctx, year, month))


@main.command(name='now-and-next')
@click.pass_context
@click.option('--time', '-t',
              default=str(datetime.now()),
              help='Current time')
@click.option('--iso', '-i',
              default=False,
              is_flag=True,
              help='Display times in ISO format')
def now_and_next(ctx, time, iso):
    operate_timetable(cli_helper.load_timetable(ctx),
                      cli_helper.now_and_next(ctx, time, iso))


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
