# coding=utf-8
# Source : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000897
import requests
from techforimpact._data.mykey import serviceKey
import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--code', action='store_true', help='코드를 출력합니다.')
args = parser.parse_args()
if args.code:
    print("(0) 대표선거명 (1)대통령,(2)국회의원,(3)시도지사,(4)구시군장,(5)시도의원,\
          (6)구시군의회의원, (7)국회의원비례대표,(8)광역의원비례대표,(9)기초의원비례대표,(10)교육의원,(11)교육감")
else:
    print("sgTypecode를 입력하면 해당 sgTypecode와 일치하는 sgId 값을 출력합니다. 여러 개 입력하고 싶으면 ,로 구분해 주세요.")

url = 'http://apis.data.go.kr/9760000/CommonCodeService/getCommonSgCodeList'
params ={'serviceKey' : serviceKey,\
         'pageNo' : '1', 'numOfRows' : '1000'}

response = requests.get(url, params=params)
xml_data = response.content.decode('utf-8')
# Parse the XML data
root = ET.fromstring(xml_data)

# Find all elements where sgTypecode is equal to INPUT and extract their sgId values
sgIds = set()
for code in input("Input the number of sgTypecode: ").split(','):
    for item in root.findall(f'.//item[sgTypecode=\"{code}\"]'):
        sgId_element = item.find('sgId')
        if sgId_element is not None:
            sgId = sgId_element.text
            sgIds.add(sgId)

# Print the sgId values
for sgId in sorted(sgIds):
    print(sgId)