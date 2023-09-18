# coding=utf-8
# Source : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000897
import requests
from mykey import serviceKey
import xml.etree.ElementTree as ET

url = 'http://apis.data.go.kr/9760000/CommonCodeService/getCommonSgCodeList'
params ={'serviceKey' : serviceKey,\
         'pageNo' : '1', 'numOfRows' : '1000'}

response = requests.get(url, params=params)
xml_data = response.content.decode('utf-8')
# Parse the XML data
root = ET.fromstring(xml_data)

# Find all elements where sgTypecode is equal to 2 and extract their sgId values
sgIds = []

for item in root.findall('.//item[sgTypecode="2"]'):
    sgId_element = item.find('sgId')
    if sgId_element is not None:
        sgId = sgId_element.text
        sgIds.append(sgId)

# Print the sgId values
for sgId in sgIds:
    print(sgId)