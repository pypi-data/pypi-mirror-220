import time

import requests

from .chrome import user_agent


def common_headers(referer: str | None = None) -> dict:
    headers = {
        'user-agent': user_agent()
    }

    if referer is not None:
        headers.update({
            'referer': referer
        })

    return headers


def holiday_info(year: int) -> list:
    headers = common_headers()

    # 1. Generate OTP
    otp_url = 'http://open.krx.co.kr/contents/COM/GenerateOTP.jspx'
    payload = {
        'bld': 'MKD/01/0110/01100305/mkd01100305_01',
        'name': 'form',
        '_': int(time.time() * 1000)  # timestamp
    }

    r = requests.get(url=otp_url, params=payload, headers=headers)

    # 2. holiday
    url = 'http://open.krx.co.kr/contents/OPN/99/OPN99000001.jspx'
    payload = {
        'search_bas_yy': str(year),
        'gridTp': 'KRX',
        'pagePath': '/contents/MKD/01/0110/01100305/MKD01100305.jsp',
        'code': r.text
    }

    r = requests.post(url=url, data=payload, headers=headers)
    json = r.json()

    holiday = [item['calnd_dd'] for item in json['block1']]

    return holiday


def get_json_data(payload: dict) -> list[dict]:
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    r = requests.post(url=url, data=payload)
    json = r.json()

    keys = list(json)
    k = keys[1] if keys[0] == 'CURRENT_DATETIME' else keys[0]

    if k != 'output' and k != 'OutBlock_1' and k != 'block1':
        raise NotImplementedError(k)

    return json[k]


def download_csv(payload: dict) -> str:
    # 1. Generate OTP
    otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'

    r = requests.post(url=otp_url, data=payload)
    otp = {
        'code': r.text
    }

    # 2. Download CSV
    url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'

    r = requests.post(url=url, data=otp)
    csv = r.content.decode(encoding='euc_kr')

    return csv
