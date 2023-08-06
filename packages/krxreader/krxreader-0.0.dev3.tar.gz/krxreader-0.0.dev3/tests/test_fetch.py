import pytest

from krxreader.chrome import major_version
from krxreader.fetch import common_headers
from krxreader.fetch import holiday_info
from krxreader.fetch import get_json_data
from krxreader.fetch import download_csv


@pytest.fixture
def payload():
    """[11001] 통계 > 기본 통계 > 지수 > 주가지수 > 전체지수 시세"""

    return {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00101',
        'locale': 'ko_KR',
        'idxIndMidclssCd': '01',
        'trdDd': '20230602',
        'share': '2',
        'money': '3',
        'csvxls_isNo': 'false'
    }


def test_common_headers():
    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
            'Chrome/{}.0.0.0 Safari/537.36'

    referer = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201'

    headers = common_headers(referer)
    assert headers['user-agent'] == agent.format(major_version())
    assert headers['referer'] == referer

    headers = common_headers()
    assert headers['user-agent'] == agent.format(major_version())
    with pytest.raises(KeyError):
        assert headers['referer'] == referer


@pytest.mark.skipif(True, reason='requires http request')
def test_holiday_info():
    info_list = holiday_info(2023)

    assert len(info_list) == 14
    assert info_list[0] == '2023-01-23'
    assert info_list[13] == '2023-12-29'


@pytest.mark.skipif(False, reason='requires http request')
def test_get_json_data(payload):
    data = get_json_data(payload)

    assert data[0]['IDX_NM'] == 'KRX 300'
    assert data[0]['CLSPRC_IDX'] == '1,573.77'


@pytest.mark.skipif(False, reason='requires http request')
def test_download_csv(payload):
    bld = payload.pop('bld')
    payload['name'] = 'fileDown'
    payload['url'] = bld

    csv = download_csv(payload)

    lines = csv.splitlines()
    first = lines[1].split(',')

    assert first[0] == '"KRX 300"'
    assert first[1] == '"1573.77"'
