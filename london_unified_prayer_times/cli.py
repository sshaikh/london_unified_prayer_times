"""Console script for london_unified_prayer_times."""
import sys
import click
from datetime import date
from datetime import datetime
import pytz

from . import cache
from . import config
from . import constants
from . import query


tk = constants.TimetableKeys
ck = constants.ConfigKeys


@click.group()
@click.option('--timetable', '-t', default=constants.PICKLE_FILENAME,
              help='Name of the local timetable to use')
@click.pass_context
def main(ctx, timetable):
    """Console script for london_unified_prayer_times."""
    ctx.ensure_object(dict)
    ctx.obj[tk.NAME] = timetable
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
        name = ctx.obj[tk.NAME]
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
        name = ctx.obj[tk.NAME]
        return cache.refresh_timetable_by_name(name)

    def operate(tt):
        click.echo(f'Successfully refreshed {tt[tk.NAME]} timetable' +
                   f' with {tt[tk.STATS][tk.NUMBER_OF_DATES]} dates')

    operate_timetable(setup, operate)


def load_timetable(ctx):
    def load_timetable():
        name = ctx.obj[tk.NAME]
        return cache.load_cached_timetable(name)
    return load_timetable


@main.command(name='list-times')
@click.pass_context
def list_times(ctx):
    def operate(tt):
        click.echo(f'{tt[tk.NAME].capitalize()} timetable contains times for:')
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
@click.option('--timezone', '-t',
              default=str(datetime.utcnow().astimezone().tzinfo),
              help='Timezone to render times in')
def show_day(ctx, requested_date, timezone):
    def operate(tt):
        dt = date.fromisoformat(requested_date)
        day = query.get_day(tt, dt)
        click.echo(f'{tt[tk.NAME].capitalize()} timetable for ' +
                   f'{dt.isoformat()}:')
        for name, time in day[tk.TIMES].items():
            local_time = time.astimezone(pytz.timezone(timezone))
            click.echo(f'{name}: {local_time.strftime("%-H:%M")}')

    operate_timetable(load_timetable(ctx), operate)


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
