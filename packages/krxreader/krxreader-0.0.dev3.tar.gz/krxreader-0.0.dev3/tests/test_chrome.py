from datetime import datetime

from krxreader.chrome import release_schedule
from krxreader.chrome import unified_platform
from krxreader.chrome import major_version
from krxreader.chrome import user_agent


def test_release_schedule():
    schedule = release_schedule()
    version = schedule[0][1]

    for item in schedule:
        assert item[1] == version
        version -= 1

    for item in schedule:
        dt = datetime.strptime(item[0], '%b %d, %Y')
        assert type(dt) is datetime


def test_unified_platform():
    assert unified_platform() == 'Macintosh; Intel Mac OS X 10_15_7'


def test_major_version():
    # assert major_version() == 114

    dt1 = datetime.fromisoformat('2023-05-30 23:59:59.283')
    assert major_version(dt1) == 113

    dt2 = datetime.fromisoformat('2023-05-31 00:00:00.000')
    assert major_version(dt2) == 114

    dt3 = datetime.fromisoformat('2023-07-18 23:59:59.283')
    assert major_version(dt3) == 114

    dt4 = datetime.fromisoformat('2023-07-19 00:00:00.000')
    assert major_version(dt4) == 115

    dt5 = datetime.fromisoformat('2025-02-05 23:59:59.283')
    assert major_version(dt5) == 133

    dt6 = datetime.fromisoformat('2023-01-11 00:00:00.000')
    assert major_version(dt6) == 109

    dt7 = datetime.fromisoformat('2023-01-10 23:59:59.283')
    assert major_version(dt7) == 100

    dt8 = datetime.fromisoformat('2000-01-01 23:59:59.283')
    assert major_version(dt8) == 100


def test_user_agent():
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/{}.0.0.0 Safari/537.36'

    result = user_agent(major_ver=1)
    assert result == agent.format(1)

    result = user_agent(major_ver=120)
    assert result == agent.format(120)

    result = user_agent()
    assert result == agent.format(major_version())


def test_maintenance():
    """If this test fails, update release_schedule() function."""

    schedule = release_schedule()
    latest_version = schedule[0][1]

    assert major_version() != latest_version
