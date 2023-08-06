import pytest

from krxreader.stock import Stock


@pytest.mark.skipif(True, reason='requires http request')
def test_search_issue():
    stock = Stock()

    item = stock.search_issue('005930')
    assert item == ('삼성전자', '005930', 'KR7005930003')

    item = stock.search_issue('삼성전자')
    assert item == ('삼성전자', '005930', 'KR7005930003')

    item = stock.search_issue('035420')
    assert item == ('NAVER', '035420', 'KR7035420009')

    item = stock.search_issue('NAVER')
    assert item == ('NAVER', '035420', 'KR7035420009')


@pytest.mark.skipif(True, reason='requires http request')
def test_stock_price():
    stock = Stock('20230519', market='ALL')
    data = stock.stock_price()

    assert data[1][0] == '060310'
    assert data[1][5] == '2,290'

    stock = Stock('20230519', market='STK')
    data = stock.stock_price()

    assert data[1][0] == '095570'
    assert data[1][5] == '4,445'

    stock = Stock('20230519', market='KSQ')
    data = stock.stock_price()

    assert data[1][0] == '060310'
    assert data[1][5] == '2,290'

    stock = Stock('20230519', market='KNX')
    data = stock.stock_price()

    assert data[1][0] == '278990'
    assert data[1][5] == '6,800'


@pytest.mark.skipif(True, reason='requires http request')
def test_stock_price_change():
    stock = Stock(start='20230517', end='20230525')
    data = stock.stock_price_change()

    assert data[1975][0] == '417500'
    assert data[1975][2] == '5,252'

    stock = Stock(start='20230517', end='20230525', adjusted_price=False)
    data = stock.stock_price_change()

    assert data[1975][0] == '417500'
    assert data[1975][2] == '21,000'


@pytest.mark.skipif(True, reason='requires http request')
def test_price_by_issue():
    stock = Stock(start='20230630', end='20230707')
    data = stock.price_by_issue('035420')  # NAVER

    assert data[0][1] == 'TDD_CLSPRC'
    assert data[1][1] == '195,000'


@pytest.mark.skipif(True, reason='requires http request')
def test_all_listed_issues():
    stock = Stock()
    data = stock.all_listed_issues()

    assert len(data[0]) == 12
    assert data[0][0] == 'ISU_CD'
    assert data[0][11] == 'LIST_SHRS'
