# -*- coding: utf-8 -*-
"""동행복권 API에서 신규 회차를 받아 data/lotto.json에 추가한다.

2026년 사이트 개편으로 구 API(common.do?method=getLottoNumber)가 폐지되어
신 API(lt645/selectPstLt645InfoNew.do)를 사용한다.
center 요청은 기준 회차 아래 5개·위 4개(총 10회차)를 반환하므로,
마지막 보유 회차를 기준으로 반복 요청해 그보다 큰 회차를 수집한다.
"""
import json, sys, urllib.request

PATH = 'data/lotto.json'
API = ('https://www.dhlottery.co.kr/lt645/selectPstLt645InfoNew.do'
       '?srchDir=center&srchLtEpsd={}')
UA = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
last = data[-1]['r']

def fetch_window(rnd):
    req = urllib.request.Request(API.format(rnd), headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=15) as res:
        return json.load(res)['data']['list']

added = 0
while True:
    try:
        rows = fetch_window(last)
    except Exception as e:
        print(f'{last}회 기준 요청 실패: {e}'); break
    new = sorted((r for r in rows if r['ltEpsd'] > last), key=lambda r: r['ltEpsd'])
    if not new:
        break  # 이후 회차 없음(최신 상태)
    for r in new:
        d = r['ltRflYmd']  # "20260905"
        data.append({
            'r': r['ltEpsd'],
            'd': f'{d[:4]}.{d[4:6]}.{d[6:]}',
            'n': sorted(r[f'tm{i}WnNo'] for i in range(1, 7)),
            'b': r['bnsWnNo'],
        })
        print(f"{r['ltEpsd']}회 추가")
        added += 1
    last = data[-1]['r']

if added:
    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f'총 {added}회차 갱신 완료')
else:
    print('신규 회차 없음')
sys.exit(0)
