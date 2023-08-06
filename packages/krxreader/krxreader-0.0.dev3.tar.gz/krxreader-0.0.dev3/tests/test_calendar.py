from datetime import datetime

import pytest

from krxreader.calendar import holiday_info
from krxreader.calendar import now
from krxreader.calendar import is_weekend
from krxreader.calendar import is_holiday
from krxreader.calendar import is_closing_day
from krxreader.calendar import is_trading_day
from krxreader.calendar import trading_date
from krxreader import fetch


def test_holiday_info():
    info = holiday_info(2022)

    assert len(info) == 14
    assert info[0] == '2022-01-31'
    assert info[13] == '2022-12-30'

    info = holiday_info(2023)

    assert len(info) == 14
    assert info[0] == '2023-01-23'
    assert info[13] == '2023-12-29'

    info = holiday_info(2024)

    assert len(info) == 0


def test_now():
    print(now())

    assert True


def test_is_weekend():
    # 토요일
    dt1 = datetime.fromisoformat('2023-06-10 00:00:00.501235+09:00')
    dt2 = datetime.fromisoformat('2023-06-10 09:00:00.501235+09:00')
    dt3 = datetime.fromisoformat('2023-06-10 23:59:59.501235+09:00')
    # 일요일
    dt4 = datetime.fromisoformat('2023-06-11 00:00:00.501235+09:00')
    dt5 = datetime.fromisoformat('2023-06-11 09:00:00.501235+09:00')
    dt6 = datetime.fromisoformat('2023-06-11 23:59:59.501235+09:00')
    # 월요일
    dt7 = datetime.fromisoformat('2023-06-12 00:00:00.501235+09:00')
    dt8 = datetime.fromisoformat('2023-06-12 09:00:00.501235+09:00')
    dt9 = datetime.fromisoformat('2023-06-12 23:59:59.501235+09:00')

    assert is_weekend(dt1) is True
    assert is_weekend(dt2) is True
    assert is_weekend(dt3) is True
    assert is_weekend(dt4) is True
    assert is_weekend(dt5) is True
    assert is_weekend(dt6) is True
    assert is_weekend(dt7) is False
    assert is_weekend(dt8) is False
    assert is_weekend(dt9) is False


@pytest.mark.skipif(False, reason='requires http request')
def test_is_holiday():
    # 공휴일
    dt1 = datetime.fromisoformat('2022-06-06 00:00:00.501235+09:00')
    dt2 = datetime.fromisoformat('2023-06-06 09:00:00.501235+09:00')
    dt3 = datetime.fromisoformat('2024-06-06 23:59:59.501235+09:00')
    # 평일
    dt4 = datetime.fromisoformat('2023-06-07 09:00:00.501235+09:00')

    assert is_holiday(dt1) is True
    assert is_holiday(dt2) is True
    assert is_holiday(dt3) is True
    assert is_holiday(dt4) is False


def test_is_closing_day():
    # 토요일
    dt1 = datetime.fromisoformat('2023-05-20 08:59:59.501235+09:00')
    # 일요일
    dt2 = datetime.fromisoformat('2023-05-21 08:59:59.501235+09:00')
    # 공휴일
    dt3 = datetime.fromisoformat('2023-06-06 08:59:59.501235+09:00')
    # 월요일
    dt4 = datetime.fromisoformat('2023-05-22 08:59:59.501235+09:00')

    assert is_closing_day(dt1) is True
    assert is_closing_day(dt2) is True
    assert is_closing_day(dt3) is True
    assert is_closing_day(dt4) is False


def test_is_trading_day():
    # 토요일
    dt1 = datetime.fromisoformat('2023-05-20 08:59:59.501235+09:00')
    # 일요일
    dt2 = datetime.fromisoformat('2023-05-21 08:59:59.501235+09:00')
    # 공휴일
    dt3 = datetime.fromisoformat('2023-06-06 08:59:59.501235+09:00')
    # 월요일
    dt4 = datetime.fromisoformat('2023-05-22 08:59:59.501235+09:00')

    assert is_trading_day(dt1) is False
    assert is_trading_day(dt2) is False
    assert is_trading_day(dt3) is False
    assert is_trading_day(dt4) is True


def test_trading_date():
    # 토요일
    dt1 = datetime.fromisoformat('2023-05-20 08:59:59.501235+09:00')
    dt2 = datetime.fromisoformat('2023-05-20 09:00:00.501235+09:00')
    dt3 = datetime.fromisoformat('2023-05-20 23:59:59.501235+09:00')

    assert trading_date(dt1) == '20230519'
    assert trading_date(dt2) == '20230519'
    assert trading_date(dt3) == '20230519'
    assert trading_date(dt1, base_time=9) == '20230519'
    assert trading_date(dt2, base_time=9) == '20230519'
    assert trading_date(dt3, base_time=9) == '20230519'
    assert trading_date(dt1, base_time=24) == '20230519'
    assert trading_date(dt2, base_time=24) == '20230519'
    assert trading_date(dt3, base_time=24) == '20230519'

    # 일요일
    dt4 = datetime.fromisoformat('2023-05-21 08:59:59.501235+09:00')
    dt5 = datetime.fromisoformat('2023-05-21 09:00:00.501235+09:00')
    dt6 = datetime.fromisoformat('2023-05-21 23:59:59.501235+09:00')

    assert trading_date(dt4) == '20230519'
    assert trading_date(dt5) == '20230519'
    assert trading_date(dt6) == '20230519'
    assert trading_date(dt4, base_time=9) == '20230519'
    assert trading_date(dt5, base_time=9) == '20230519'
    assert trading_date(dt6, base_time=9) == '20230519'
    assert trading_date(dt4, base_time=24) == '20230519'
    assert trading_date(dt5, base_time=24) == '20230519'
    assert trading_date(dt6, base_time=24) == '20230519'

    # 월요일
    dt7 = datetime.fromisoformat('2023-05-22 08:59:59.501235+09:00')
    dt8 = datetime.fromisoformat('2023-05-22 09:00:00.501235+09:00')
    dt9 = datetime.fromisoformat('2023-05-22 23:59:59.501235+09:00')

    assert trading_date(dt7) == '20230522'
    assert trading_date(dt8) == '20230522'
    assert trading_date(dt9) == '20230522'
    assert trading_date(dt7, base_time=9) == '20230519'
    assert trading_date(dt8, base_time=9) == '20230522'
    assert trading_date(dt9, base_time=9) == '20230522'
    assert trading_date(dt7, base_time=24) == '20230519'
    assert trading_date(dt8, base_time=24) == '20230519'
    assert trading_date(dt9, base_time=24) == '20230519'


@pytest.mark.skipif(False, reason='requires http request')
def test_maintenance():
    """If this test fails, update holiday_info() function."""

    dt = now()

    assert holiday_info(dt.year) == fetch.holiday_info(dt.year)
