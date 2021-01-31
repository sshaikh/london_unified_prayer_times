"""Console script for london_unified_prayer_times."""
import sys
import click

from . import cache
from . import config
from . import constants


tk = constants.TimetableKeys


@click.group()
@click.option('--timetable', '-t', default=constants.PICKLE_FILENAME,
              help='Local name of the timetable to use')
@click.pass_context
def main(ctx, timetable):
    """Console script for london_unified_prayer_times."""
    ctx.ensure_object(dict)
    ctx.obj[tk.NAME] = timetable
    return 0


@main.command()
@click.pass_context
@click.option('--url', '-u', help='URL to retrive timetable from',
              required=True)
def init(ctx, url):
    name = ctx.obj[tk.NAME]
    tt = cache.init_timetable(name,
                              url,
                              config.default_config,
                              config.lupt_schema)
    if tt:
        click.echo(f'Successfully initialised {tt[tk.NAME]}' +
                   f' with {tt[tk.NUMBER_OF_DATES]} dates' +
                   f' from {tt[tk.SOURCE]}')
        return 0
    return -1


@main.command()
@click.pass_context
def refresh(ctx):
    name = ctx.obj[tk.NAME]
    tt = cache.refresh_timetable_by_name(name)
    if tt:
        click.echo(f'Successfully refreshed {tt[tk.NAME]}' +
                   f' with {tt[tk.NUMBER_OF_DATES]} dates')
        return 0

    return -1


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
