import pytest
from london_unified_prayer_times import remote_data
from london_unified_prayer_times import config


@pytest.mark.vcr()
def test_get_json_data():
    url = ("https://mock.location.com/lupt")
    json = remote_data.get_json_data(url, config.lupt_schema)
    assert json is not None
