from .base import KrxBase


class Bond(KrxBase):
    def __init__(self, date, start=None, end=None, market='KTS', money='2'):
        super().__init__(date, start, end)

        # 'KTS': 국채전문유통시장, 'BND': 일반채권시장, 'SMB': 소액채권시장
        self._market = market
        # '1':원, '2':천원, '3':백만원, '4':십억원
        self._money = money

    def bond_price(self):
        """[14001] 채권 > 종목시세 > 전종목 시세
        :return:
        """
        bld = 'dbms/MDC/STAT/standard/MDCSTAT09801'

        params = {
            'mktId': self._market,
            'trdDd': self._date,
            'money': self._money
        }

        return self.fetch_data(bld, params)

    def all_listed_issues(self, bond_type='TT'):
        """[14003] 채권 > 종목정보 > 전종목 기본정보
        :param bond_type: str
            'TT': 전체
            'GB': 국채
            'MB': 지방채
            'AB': 특수채
            'CO': 회사채
            'FO': 외국채
        :return:
        """
        bld = 'dbms/MDC/STAT/standard/MDCSTAT10001'

        params = {
            'bndTpCd': bond_type,
            'money': self._money
        }

        return self.fetch_data(bld, params)
