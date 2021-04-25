import pytest
from london_unified_prayer_times import remote_data


@pytest.mark.vcr()
def test_get_html_data():
    url = ("https://mock.location.com/prayer-times")
    data = remote_data.get_html_data(url, "Prayerdata")
    assert data is not None
