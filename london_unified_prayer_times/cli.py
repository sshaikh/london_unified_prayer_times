"""Console script for london_unified_prayer_times."""
import sys
import click

from . import cache
from . import config
from . import constants


@click.group()
def main(args=None):
    """Console script for london_unified_prayer_times."""
    return 0


@main.command()
# @main.option('--url', '-u', help='URL to retrieve times from')
def refresh():
    url = 'plop'
    schema = config.lupt_schema
    pickle_filename = constants.PICKLE_FILENAME
    tt = cache.refresh_timetable(url, schema, config, pickle_filename)
    if tt:
        num_dates = len(tt[constants.TimetableKeys.DATES])
        click.echo(f'Successfully refreshed {num_dates}' +
                   ' dates into ' +
                   pickle_filename)
        return 0

    return -1


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
