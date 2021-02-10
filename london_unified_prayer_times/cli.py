"""Console script for london_unified_prayer_times."""
import sys
import click
from click_default_group import DefaultGroup
from datetime import date
from datetime import datetime
from tzlocal import get_localzone

from . import cache
from . import config
from . import constants
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
@click.option('--replace', '-r', 'replace_strings',
              nargs=2, type=str,
              multiple=True,
              default=[],
              help="Replace strings")
@click.option('--cache-expiry', '-c',
              type=int,
              default=None,
              help='Override configured cache expiry (weeks)')
@click.pass_context
def main(ctx, timetable, hours, timezone, time_filter,
         replace_strings, cache_expiry):
    """Console script for london_unified_prayer_times."""
    ctx.ensure_object(dict)
    ctx.obj[clk.NAME] = timetable
    ctx.obj[clk.TIMEZONE] = timezone
    ctx.obj[clk.HOURS] = hours
    ctx.obj[clk.USE_TIMES] = time_filter
    ctx.obj[clk.REPLACE_STRINGS] = replace_strings
    ctx.obj[clk.CACHE_EXPIRY] = cache_expiry
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


@main.command(name='show-info')
@click.pass_context
def show_info(ctx):
    operate_timetable(cli_helper.load_timetable(ctx),
                      cli_helper.show_info)


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
