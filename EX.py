from bs4 import BeautifulSoup as BS
import ssl
from urllib import parse
from urllib import request
import traceback

target = input("검색어 입력")

base_url = 'https://www.google.co.kr/search'
#: 검색조건 설정
values = { 'q': target, # 검색할 내용
           'oq': target,
           'aqs': 'chrome..69i57.35694j0j7',
           'sourceid': 'chrome', 'ie': 'UTF-8',
           }
# Google에서는 Header 설정 필요
hdr = {'User-Agent': 'Mozilla/5.0'}

query_string = parse.urlencode(values)
req = request.Request(base_url + '?' + query_string, headers=hdr)
context = ssl._create_unverified_context()
try:
    res = request.urlopen(req, context=context)
except:
    traceback.print_exc()

html_data = BS(res.read(), 'html.parser')
#print(html_data)

g_list = html_data.find_all('div', attrs={'class': 'g'})
try:
    for g in g_list:
        # 컨텐츠 URL 꺼내기
        ahref = g.find('a')['href']
        print(str(ahref))
        ahref = 'https://www.google.co.kr' + ahref
        print(ahref)
        
        # 컨텐츠에서 검색결과와 일치하는 부분 꺼내기
        span = g.find('span', attrs = {'class': 'st'})
        print(span)
        if span:
            span_text = span.get_text()
            print(span_text)

            span_text = span_text.replace(' ', '')
            print(span_text)

            span_text = span_text.replace('\n', '')
            print(span_text)
except:
    traceback.print_exc()

