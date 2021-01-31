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


def test_refresh_database_default(three_day_timetable_mock):
    assert_cli(['refresh'],
               'Successfully refreshed 3 dates into timetable')


def test_refresh_database_named(three_day_timetable_mock):
    assert_cli(['--timetable', 'test_table', 'refresh'],
               'Successfully refreshed 3 dates into test_table')
