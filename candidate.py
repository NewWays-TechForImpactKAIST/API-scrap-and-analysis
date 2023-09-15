# coding=utf-8
# Source : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000908
import requests
from mykey import serviceKey

url = 'http://apis.data.go.kr/9760000/PofelcddInfoInqireService/getPoelpcddRegistSttusInfoInqire'
params ={'serviceKey' : serviceKey,\
         'pageNo' : '1', 'numOfRows' : '10', 'sgId' : '20220601', 'sgTypecode' : '4', 'sggName' : '', 'sdName' : '', 'jdName' : ''}

response = requests.get(url, params=params)
print(response.content.decode('utf-8'))