#!/usr/bin/env python

"""Tests for `london_unified_prayer_times` package."""

import pytest

from click.testing import CliRunner

from london_unified_prayer_times import london_unified_prayer_times as lupt
from london_unified_prayer_times import cli


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'london_unified_prayer_times.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


@pytest.mark.vcr()
def test_get_json_data():
    url = ("https://mock.location.com/lupt")
    json = lupt.get_json_data(url)
    assert json is not None
