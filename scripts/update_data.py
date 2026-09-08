# -*- coding: utf-8 -*-
"""동행복권 API에서 신규 회차를 받아 data/lotto.json에 추가한다."""
import json, sys, urllib.request

PATH = 'data/lotto.json'
API = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}'

with open(PATH, encoding='utf-8') as f:
    data = json.load(f)
last = data[-1]['r']

added = 0
rnd = last + 1
while True:
    try:
        with urllib.request.urlopen(API.format(rnd), timeout=10) as res:
            j = json.load(res)
    except Exception as e:
        print(f'{rnd}회 요청 실패: {e}'); break
    if j.get('returnValue') != 'success':
        break  # 아직 추첨 전
    data.append({
        'r': j['drwNo'],
        'd': j['drwNoDate'].replace('-', '.'),
        'n': sorted([j[f'drwtNo{i}'] for i in range(1, 7)]),
        'b': j['bnusNo'],
    })
    print(f"{j['drwNo']}회 추가")
    added += 1
    rnd += 1

if added:
    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))
    print(f'총 {added}회차 갱신 완료')
else:
    print('신규 회차 없음')
sys.exit(0)
