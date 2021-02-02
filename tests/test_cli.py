from click.testing import CliRunner

from london_unified_prayer_times import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'Show this message and exit.' in result.output
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
               'Default timetable contains times for:\nsunrise')


def test_list_dates(cache_mock):
    pass


def test_show_day(cache_mock):
    assert_cli(['show-day', '--date', '2020-10-02'],
               'Default timetable for 2020-10-02:\nsunrise: 6:00')


def test_show_day_today(cache_mock):
    pass
#    assert_cli(['show-day'],
#               'Default timetable for 20201002:\nsunrise: 2020')


def test_show_calendar():
    pass


def test_show_calendar_today():
    pass


def test_now_next():
    pass


def test_now_next_now():
    pass


def test_debug():
    pass
