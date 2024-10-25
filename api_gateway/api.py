from urllib.parse import urlencode, unquote, quote_plus

import requests
from bs4 import BeautifulSoup

serviceKey = "diUBgK2%2Bo8yKd9Ki8Fl2h6GNrzg%2B0guxZ0TDHh%2FhZs0xwT6wg4iDIhSRw9Yy6z%2FBqzX76zT%2FmycLL9P6gSNppQ%3D%3D"
serviceKeyDecoded = unquote(serviceKey, 'UTF-8')

def check_air():
    station = []
    pm10 = []
    url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty"
    returnType="xml"
    numOfRows="100"
    pageNo="1"
    sidoName="서울"
    ver="1.0"

    queryParams = '?' + urlencode({ quote_plus('ServiceKey') : serviceKeyDecoded, quote_plus('returnType') : returnType, quote_plus('numOfRows') : numOfRows, quote_plus('pageNo') : pageNo, quote_plus('sidoName') : sidoName, quote_plus('ver') : ver })
    res = requests.get(url + queryParams)
    xml = res.text
    soup = BeautifulSoup(xml, 'html.parser')
    for tag in soup.find_all('stationname'):
        station.append(tag.text)
    for tag in soup.find_all('pm10value'):
        pm10.append(tag.text)
    res = dict(zip(station, pm10))
    return res
