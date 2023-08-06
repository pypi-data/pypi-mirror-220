import datetime

import pytest

from krxreader.index import StockIndex
from krxreader.index import BondIndex
from krxreader.calendar import is_closing_day
from krxreader.calendar import now


class TestStockIndex:
    def test_index_price(self):
        index = StockIndex('20230519')
        data = index.index_price()

        assert data[1][0] == 'KRX 300'
        assert data[1][1] == '1533.13'

    def test_index_price_change(self):
        index = StockIndex(start='20230511', end='20230519')
        data = index.index_price_change()

        assert data[1][0] == 'KRX 300'
        assert data[1][2] == '1533.13'

    def test_price_by_index(self):
        index = StockIndex(start='20230511', end='20230519')
        data = index.price_by_index('KTOP 30')

        assert data[1][0] == '2023/05/19'
        assert data[1][1] == '8986.38'

    def test_all_indices(self):
        index = StockIndex()
        data = index.all_indices()

        assert data[1][0] == 'KRX 300'
        assert data[1][2] == '2010.01.04'


class TestBondIndex:
    def test_date(self):
        index = BondIndex(end='20230623')
        assert index._start == '20230616'

        index = BondIndex(end='20230607')
        assert index._start == '20230531'

        index = BondIndex(end='20230605')
        assert index._start == '20230526'

        index = BondIndex(end='20230602')
        assert index._start == '20230526'

        index = BondIndex(end='20230601')
        assert index._start == '20230525'

    def test_date_now(self):
        dt = now()

        dt = dt - datetime.timedelta(days=1)
        while is_closing_day(dt):
            dt = dt - datetime.timedelta(days=1)

        date = dt.strftime('%Y%m%d')

        dt = dt - datetime.timedelta(days=7)
        while is_closing_day(dt):
            dt = dt - datetime.timedelta(days=1)

        start = dt.strftime('%Y%m%d')

        print(f'{start} ~ {date}')

        index = BondIndex()

        assert index._date == date
        assert index._end == date
        assert index._start == start

    @pytest.mark.skipif(True, reason='requires http request')
    def test_index_price(self):
        index = BondIndex('20230526')
        data = index.index_price()

        assert data[1][0] == 'KRX 채권지수'
        assert data[1][1] == '180.37'
        assert data[2][0] == 'KTB 지수'
        assert data[2][1] == '14,661.86'
        assert data[3][0] == '국고채프라임지수'
        assert data[3][1] == '181.05'

    @pytest.mark.skipif(True, reason='requires http request')
    def test_price_by_index(self):
        index = BondIndex(start='20230519', end='20230526')
        data = index.price_by_index()

        assert data[1][0] == '2023/05/26'
        assert data[1][1] == '180.37'

        data = index.price_by_index('국고채프라임지수')

        assert data[1][0] == '2023/05/26'
        assert data[1][1] == '181.05'

    @pytest.mark.skipif(False, reason='requires http request')
    def test_maintenance(self):
        """If this test fails, update index_table of price_by_index() function."""

        index = BondIndex()
        data = index.index_price()

        assert len(data) == 4
        assert len(data[0]) == 19
