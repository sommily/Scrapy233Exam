# -*- coding: utf-8 -*-
__author__ = "Sommily"

import json
import requests
from hashlib import md5
from random import randrange
from datetime import datetime

REQUEST_URL = "https://japi.233.com/ess-tiku-api/front/extract/page"
USER_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIzMjQzOTM1NyIsInVuaW9uSWQiOiIwMDAwMDEiLCJib3NzTmFtZSI6IiIsInJvbGVDb2RlcyI6bnVsbCwidXNlck5hbWUiOiJsbTEzMTk4NTMyNzA1IiwidXNlcklkIjoiMzI0MzkzNTciLCJoZWFkUGljIjoiaHR0cDovL2ltZy4yMzMuY29tL3d4L2ltZy91Yy9BdmF0YXIucG5nIiwicGxhdGZvcm0iOjAsInJvbGVJZHMiOltdLCJuaWNrbmFtZSI6IiIsInVzZXJUeXBlIjoxLCJleHAiOjE2ODIzMzA3NTIsImlhdCI6MTY4MTQ2Njc1MiwianRpIjoiNDMwM2NhNDMtMDk2MS00NjdlLWJjNWUtZGZmMDBjMjM3ZDFiIn0.gkL9ZS1wB1ja6Cx4mNLISMKHG7RWlJ-cP565Tpil06Y"
ZT_NO = "ZT2304141920068108210166"

sid_date = datetime.now().strftime('%Y%m%d%H%M%S')
sid_date = f"{sid_date[:4]}{datetime.now().month - 1:02d}{sid_date[6:]}"
sid = f"ucpage{sid_date}{randrange(10000, 99999)}{randrange(10000, 99999)}"
params = {"pageSize": 150, "pageNo": 1, "ztNo": ZT_NO}
m = md5()
m.update(f"RZRRNN9RXYCP{sid}{json.dumps(params).replace(' ', '')}".encode("utf-8"))
sign = m.hexdigest().upper()

print("sid", sid)
print("sign", sign)

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    "Content-Type": "application/json",
    'DNT': '1',
    'Origin': 'https://wx.233.com',
    'Pragma': 'no-cache',
    'Referer': 'https://wx.233.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    "sid": sid,
    "sign": sign,
    "token": USER_TOKEN
}

resp = requests.post(url=REQUEST_URL, headers=headers, data=json.dumps(params).replace(' ', ''))

title = resp.json().get("data", {}).get("title", "X")
json.dump(obj=resp.json(), fp=open(f"/Users/Sommily/tmp/{title}.json", "w"), indent=4)
