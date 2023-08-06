from .base import KrxBase


class StockIndex(KrxBase):
    """통계 > 기본 통계 > 지수 > 주가지수

    :param date: 조회일자
    :param start: 조회기간
    :param end: 조회기간
    :param sector: '01': KRX, '02': KOSPI, '03': KOSDAQ, '04': 테마
    :param share: '1': 주, '2': 천주, '3': 백만주
    :param money: '1': 원, '2': 천원, '3': 백만원, '4': 십억원
    """

    def __init__(
            self,
            date: str | None = None,
            start: str | None = None,
            end: str | None = None,
            sector: str = '01',
            share: str = '2',
            money: str = '3'
    ):
        super().__init__(date, start, end)

        self._sector = sector
        self._share = share
        self._money = money

    def index_price(self) -> list[list]:
        """[11001] 통계 > 기본 통계 > 지수 > 주가지수 > 전체지수 시세"""

        bld = 'dbms/MDC/STAT/standard/MDCSTAT00101'
        params = {
            'idxIndMidclssCd': self._sector,
            'trdDd': self._date,
            'share': self._share,
            'money': self._money
        }

        return self.fetch_data(bld, params)

    def index_price_change(self) -> list[list]:
        """[11002] 통계 > 기본 통계 > 지수 > 주가지수 > 전체지수 등락률"""

        bld = 'dbms/MDC/STAT/standard/MDCSTAT00201'
        params = {
            'idxIndMidclssCd': self._sector,
            'strtDd': self._start,
            'endDd': self._end,
            'share': self._share,
            'money': self._money
        }

        return self.fetch_data(bld, params)

    def price_by_index(self, index_code: str) -> list[list]:
        """[11003] 통계 > 기본 통계 > 지수 > 주가지수 > 개별지수 시세 추이"""

        (item_name, item_code, full_code) = self.search_item('stock_index', index_code)

        bld = 'dbms/MDC/STAT/standard/MDCSTAT00301'
        params = {
            'tboxindIdx_finder_equidx0_0': item_name,
            'indIdx': full_code,
            'indIdx2': item_code,
            'codeNmindIdx_finder_equidx0_0': item_name,
            'param1indIdx_finder_equidx0_0': '',
            'strtDd': self._start,
            'endDd': self._end,
            'share': self._share,
            'money': self._money
        }

        return self.fetch_data(bld, params)

    def all_indices(self) -> list[list]:
        """[11004] 통계 > 기본 통계 > 지수 > 주가지수 > 전체지수 기본정보"""

        bld = 'dbms/MDC/STAT/standard/MDCSTAT00401'
        params = {
            'idxIndMidclssCd': self._sector
        }

        return self.fetch_data(bld, params)

    def summary_by_index(self) -> list[list]:
        """[11005] 통계 > 기본 통계 > 지수 > 주가지수 > 개별지수 종합정보"""
        pass

    def index_consituents(self) -> list[list]:
        """[11006] 통계 > 기본 통계 > 지수 > 주가지수 > 지수구성종목"""
        pass

    def PER_PBR_Dividend_yield(self) -> list[list]:
        """[11007] 통계 > 기본 통계 > 지수 > 주가지수 > PER/PBR/배당수익률"""
        pass


class BondIndex(KrxBase):
    """통계 > 기본 통계 > 지수 > 채권지수

    :param date: 조회일자
    :param start: 조회기간
    :param end: 조회기간
    """

    def __init__(
            self,
            date: str | None = None,
            start: str | None = None,
            end: str | None = None
    ):
        super().__init__(date, start, end, open_time=24, start_days=7)

    def index_price(self) -> list[list]:
        """[11008] 통계 > 기본 통계 > 지수 > 채권지수 > 전체지수 시세"""

        bld = 'dbms/MDC/STAT/standard/MDCSTAT00801'
        params = {
            'trdDd': self._date
        }

        return self.fetch_data(bld, params)

    def price_by_index(self, index_name: str = 'KRX채권지수') -> list[list]:
        """[11009] 통계 > 기본 통계 > 지수 > 채권지수 > 개별지수 시세 추이"""

        index_table = {
            'KRX채권지수': '1',
            'KTB지수': '3',
            '국고채프라임지수': '2'
        }

        bld = 'dbms/MDC/STAT/standard/MDCSTAT00901'
        params = {
            'indTp': index_table[index_name],
            'strtDd': self._start,
            'endDd': self._end
        }

        return self.fetch_data(bld, params)
