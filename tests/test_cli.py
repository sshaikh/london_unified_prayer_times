from click.testing import CliRunner

from london_unified_prayer_times import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert '--help  Show this message and exit.' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_refresh_database(three_day_timetable, mocker):

    mocker.patch('london_unified_prayer_times.cli.cache.refresh_timetable',
                 return_value=three_day_timetable)

    runner = CliRunner()
    result = runner.invoke(cli.main, ['refresh'])
    assert result.exit_code == 0
    assert 'Successfully refreshed 3 dates into timetable' in result.output
