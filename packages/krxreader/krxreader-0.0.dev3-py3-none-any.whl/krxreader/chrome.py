import datetime


def release_schedule() -> tuple:
    """Chromium release schedule

    https://chromiumdash.appspot.com/schedule
    """
    schedule = (
        ('Feb 4, 2025', 133),
        ('Jan 7, 2025', 132),
        ('Nov 19, 2024', 131),
        ('Oct 22, 2024', 130),
        ('Sep 24, 2024', 129),
        ('Aug 27, 2024', 128),
        ('Jul 30, 2024', 127),
        ('Jun 18, 2024', 126),
        ('May 21, 2024', 125),
        ('Apr 23, 2024', 124),
        ('Mar 26, 2024', 123),
        ('Feb 27, 2024', 122),
        ('Jan 30, 2024', 121),
        ('Jan 2, 2024', 120),
        ('Nov 7, 2023', 119),
        ('Oct 10, 2023', 118),
        ('Sep 12, 2023', 117),
        ('Aug 15, 2023', 116),
        ('Jul 18, 2023', 115),
        ('May 30, 2023', 114),
        ('May 2, 2023', 113),
        ('Apr 4, 2023', 112),
        ('Mar 7, 2023', 111),
        ('Feb 7, 2023', 110),
        ('Jan 10, 2023', 109)
    )

    return schedule


def unified_platform() -> str:
    """platform part of user-agent

    macOS:   'Macintosh; Intel Mac OS X 10_15_7'
    windows: 'Windows NT 10.0; Win64; x64'
    linux:   'X11; Linux x86_64'

    https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/content/common/user_agent.cc
    """
    platform = 'Macintosh; Intel Mac OS X 10_15_7'

    return platform


def major_version(now: datetime.datetime | None = None) -> int:
    """Major version of Chrome Browser"""

    if now is None:
        now = datetime.datetime.utcnow()

    schedule = release_schedule()
    version = 100

    for item in schedule:
        if now.date() > datetime.datetime.strptime(item[0], '%b %d, %Y').date():
            version = item[1]
            break

    return version


def user_agent(major_ver: int | None = None) -> str:
    """Return the user-agent of Chrome Browser"""

    if major_ver is None:
        major_ver = major_version()

    agent = 'Mozilla/5.0 ({}) AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/{}.0.0.0 Safari/537.36'

    return agent.format(unified_platform(), major_ver)
