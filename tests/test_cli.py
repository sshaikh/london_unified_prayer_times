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
                '--config', 'config'],
               'Successfully initialised pytest timetable ' +
               'with 3 dates from conftest.py')


def test_refresh(cache_mock):
    assert_cli(['refresh'],
               'Successfully refreshed pytest timetable with 3 dates')
