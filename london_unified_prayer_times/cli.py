"""Console script for london_unified_prayer_times."""
import sys
import click

from . import cache
from . import config
from . import constants


@click.group()
@click.option('--timetable', '-t', default=constants.PICKLE_FILENAME)
@click.pass_context
def main(ctx, timetable):
    """Console script for london_unified_prayer_times."""
    ctx.ensure_object(dict)
    ctx.obj['timetable'] = timetable
    return 0


@main.command()
@click.pass_context
# @main.option('--url', '-u', help='URL to retrieve times from')
def refresh(ctx):
    url = 'plop'
    schema = config.lupt_schema
    pickle_filename = ctx.obj['timetable']
    tt = cache.init_timetable(url, schema, config, pickle_filename)
    if tt:
        num_dates = len(tt[constants.TimetableKeys.DATES])
        click.echo(f'Successfully refreshed {num_dates}' +
                   ' dates into ' +
                   pickle_filename)
        return 0

    return -1


if __name__ == "__main__":
    sys.exit(main(obj={}))  # pragma: no cover
