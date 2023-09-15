# coding=utf-8
# Source : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000897
import requests
from mykey import serviceKey

url = 'http://apis.data.go.kr/9760000/CommonCodeService/getCommonSgCodeList'
params ={'serviceKey' : serviceKey,\
         'pageNo' : '1', 'numOfRows' : '1000'}

response = requests.get(url, params=params)
print(response.content.decode('utf-8'))