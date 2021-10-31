"""Console script for london_unified_prayer_times."""
import sys
import click
from click_default_group import DefaultGroup
from datetime import date
from datetime import datetime
from tzlocal import get_localzone
from zoneinfo import ZoneInfo
from datetime import timedelta

from . import cache
from . import config
from . import constants
from . import query
from . import report


clk = constants.ClickKeys


@click.group(cls=DefaultGroup, default='now-and-next', default_if_no_args=True)
@click.option('--timetable', '-t', default=constants.DEFAULT_TIMETABLE,
              help='Name of the local timetable to use')
@click.option('--12h/--24h', 'hours', default=False,
              help='Render times in 24h or 12h')
@click.option('--timezone', '-tz',
              default=get_localzone(),
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
@click.version_option()
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


@main.command()
@click.pass_context
@click.option('--url', '-u', required=True,
              help='URL to retrive timetable from')
@click.option('--config', '-c', 'config_file',
              help='Location of custom config')
def init(ctx, url, config_file):
    name = ctx.obj[clk.NAME]
    safe_config = config.load_config(config_file)
    tt = cache.init_timetable(name,
                              url,
                              safe_config)

    info = query.get_info(tt)

    click.echo(f'Successfully initialised {info[0]} timetable'
               f' with {info[2][0]} dates'
               f' from {info[1]}')


@main.command()
@click.pass_context
def refresh(ctx):
    name = ctx.obj[clk.NAME]
    tt = cache.refresh_timetable_by_name(name)

    info = query.get_info(tt)

    click.echo(f'Successfully refreshed {info[0]} timetable'
               f' with {info[2][0]} dates')


def load_timetable(ctx):
    cache_expiry = ctx.obj[clk.CACHE_EXPIRY]
    expiry = (timedelta(weeks=cache_expiry) if cache_expiry else None)
    return cache.load_timetable(ctx.obj[clk.NAME], expiry)


@main.command(name='show-info')
@click.pass_context
def show_info(ctx):
    tt = load_timetable(ctx)
    click.echo(report.show_info(tt))


def operate_timetable(ctx, operate):
    tt = load_timetable(ctx)
    if tt:
        times = ctx.obj[clk.USE_TIMES]
        replace_strings = ctx.obj[clk.REPLACE_STRINGS]
        hours = ctx.obj[clk.HOURS]
        tz = ZoneInfo(ctx.obj[clk.TIMEZONE])
        click.echo(operate(tt, times, replace_strings, hours, tz))


@main.command(name='show-day')
@click.pass_context
@click.option('--date', '-d', 'requested_date',
              default=date.today().isoformat(),
              help='Date to show times for (defaults to today)')
def show_day(ctx, requested_date):
    def show_day(tt, times, replace_strings, hours, tz):
        dt = date.fromisoformat(requested_date)
        return report.show_day(tt, dt,
                               times, replace_strings, hours, tz)

    operate_timetable(ctx, show_day)


@main.command(name='show-calendar')
@click.pass_context
@click.option('--year', '-y',
              default=date.today().year,
              help='Year to render calendar for')
@click.option('--month', '-m',
              default=date.today().month,
              help='Month number to render calendar for')
def show_calendar(ctx, year, month):
    def show_calendar(tt, times, replace_strings, hours, tz):
        return report.show_calendar(tt, year, month,
                                    times, replace_strings, hours, tz)

    operate_timetable(ctx, show_calendar)


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
    def now_and_next(tt, times, replace_strings, hours, tz):
        safe_time = datetime.fromisoformat(time).astimezone(tz)
        return report.now_and_next(tt, safe_time, iso, times,
                                   replace_strings, hours, tz)

    operate_timetable(ctx, now_and_next)


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
