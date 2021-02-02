from click.testing import CliRunner

from london_unified_prayer_times import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)

    # default command tries to show-day for today, so will fail
    # as probably not in test data. Expect this instead of
    # mocking today()
    assert result.exit_code == 1

    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'Show this message and exit.' in help_result.output


def assert_cli(args, expected):
    runner = CliRunner()
    result = runner.invoke(cli.main, args)
    assert result.exit_code == 0
    assert expected in result.output


def test_init(cache_mock):
    assert_cli(['init',
                '--url', 'test_source',
                '--config', 'config',
                '--schema', 'schema'],
               'Successfully initialised default timetable ' +
               'with 3 dates from conftest.py')


def test_refresh(cache_mock):
    assert_cli(['refresh'],
               'Successfully refreshed default timetable with 3 dates')


def test_list_times(cache_mock):
    assert_cli(['list-times'],
               'Default timetable contains times for:\nfajrbegins')


def test_list_dates(cache_mock):
    assert_cli(['list-dates'],
               'Default timetable contains 3 dates between ' +
               '2020-10-01 and 2020-10-03')


def test_show_day(cache_mock):
    assert_cli(['show-day', '--date', '2020-10-01'],
               'Default timetable for 2020-10-01:\nfajrbegins: 4:31')


def test_show_day_tz(cache_mock):
    assert_cli(['show-day', '--date', '2020-10-01', '--timezone', 'CET'],
               'Default timetable for 2020-10-01:\nfajrbegins: 6:31')


def test_show_calendar():
    pass


def test_show_calendar_tz():
    pass


def test_now_next():
    pass


def test_dump():
    pass
