"""Console script for london_unified_prayer_times."""
import sys
import click

from . import cache
from . import config
from . import constants
from . import query


tk = constants.TimetableKeys
ck = constants.ConfigKeys


@click.group()
@click.option('--timetable', '-t', default=constants.PICKLE_FILENAME,
              help='Local name of the timetable to use')
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
        click.echo(f'Successfully initialised {tt[tk.NAME]}' +
                   f' with {tt[tk.NUMBER_OF_DATES]} dates' +
                   f' from {tt[tk.SOURCE]}')

    operate_timetable(setup, operate)


@main.command()
@click.pass_context
def refresh(ctx):
    def setup():
        name = ctx.obj[tk.NAME]
        return cache.refresh_timetable_by_name(name)

    def operate(tt):
        click.echo(f'Successfully refreshed {tt[tk.NAME]}' +
                   f' with {tt[tk.NUMBER_OF_DATES]} dates')

    operate_timetable(setup, operate)


@main.command()
@click.pass_context
def times(ctx):
    def setup():
        name = ctx.obj[tk.NAME]
        return cache.load_cached_timetable(name)

    def operate(tt):
        click.echo(f'{tt[tk.NAME]} contains times for:')
        for time in query.get_available_times(tt):
            click.echo(time)

    operate_timetable(setup, operate)


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
