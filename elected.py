# coding=utf-8
# Source : https://www.data.go.kr/data/15000864/openapi.do#/tab_layer_detail_function
import requests
from mykey import serviceKey

url = 'http://apis.data.go.kr/9760000/WinnerInfoInqireService2/getWinnerInfoInqire'
params ={'serviceKey' : serviceKey,\
         'pageNo' : '1', 'numOfRows' : '10', 'sgId' : '20230405', 'sgTypecode' : '2', 'sdName' : '전라북도', 'sggName' : '전주시을', 'jdName' : ''}

response = requests.get(url, params=params)
print(response.content.decode('utf-8'))