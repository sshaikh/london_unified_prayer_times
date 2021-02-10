from click.testing import CliRunner

from london_unified_prayer_times import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output


def assert_cli(args, expected):
    runner = CliRunner()
    result = runner.invoke(cli.main, args)
    assert result.exit_code == 0
    assert expected in result.output
    return result


def test_init(cache_mock):
    assert_cli(['init',
                '--url', 'test_source',
                '--config', 'config',
                '--schema', 'schema'],
               'Successfully initialised pytest timetable ' +
               'with 3 dates from conftest.py')


def test_refresh(cache_mock):
    assert_cli(['refresh'],
               'Successfully refreshed pytest timetable with 3 dates')


def test_timetable_info(cache_mock):
    ret = assert_cli(['show-info'],
                     '3 dates available between ' +
                     '2020-10-01 and 2020-10-03')
    assert 'the following times:\n\nfajr' in ret.output


def test_show_day(cache_mock):
    assert_cli(['show-day', '--date', '2020-10-01'],
               ('Pytest timetable for Oct 01 (14 Safar 1442):\n\n'
               'fajr:      05:31'))


def test_show_day_replace(cache_mock):
    assert_cli(['--replace', 'fajr', 'jraf',
                'show-day', '--date', '2020-10-01'],
               ('Pytest timetable for Oct 01 (14 Safar 1442):\n\n'
               'jrafbegins:      05:31'))


def test_show_day_time_filter(cache_mock):
    assert_cli(['--use-time', 'zuhrbegins',
                'show-day', '--date', '2020-10-01'],
               'Pytest timetable for Oct 01 (14 Safar 1442):\n\nzuhr:')


def test_show_day_am(cache_mock):
    assert_cli(['--12h', 'show-day', '--date', '2020-10-01'],
               ('Pytest timetable for Oct 01 (14 Safar 1442):\n\n'
               'fajr:       5:31 am'))


def test_show_day_tz(cache_mock):
    assert_cli(['--timezone', 'CET', 'show-day', '--date', '2020-10-01'],
               ('Pytest timetable for Oct 01 (14 Safar 1442):\n\n'
                'fajr:      06:31'))


def test_show_calendar(cache_mock):
    result = assert_cli(['show-calendar', '--year', '2020', '--month', '10'],
                        ('Pytest timetable for October 2020 (Safar 1442):\n\n'
                         'date    islamic date       fajr'))
    assert '   2    15 Safar           05:32' in result.output


def test_now_next(cache_mock):
    assert_cli(['--use-time', 'fajrbegins',
                '--use-time', 'zuhrbegins',
                'now-and-next', '--time', '2020-10-02 06:00'],
               ('fajr was 28 minutes ago\n'
                'zuhr is 6 hours from now'))


def test_now_next_iso(cache_mock):
    assert_cli(['--use-time', 'fajrbegins',
                '--use-time', 'zuhrbegins',
                'now-and-next', '--time', '2020-10-02 06:00',
                '--iso'],
               ('fajr 05:32\n'
                'zuhr 12:55'))
