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


def test_init_timetable(cache_mock):
    assert_cli(['init',
                '--url', 'test_source',
                '--config', 'config',
                '--schema', 'schema'],
               'Successfully initialised timetable ' +
               'with 3 dates from conftest.py')


def test_refresh_timetable(cache_mock):
    assert_cli(['refresh'],
               'Successfully refreshed timetable with 3 dates')


def test_query_timetable(cache_mock):
    assert_cli(['times'],
               'timetable contains times for:\nsunrise')
