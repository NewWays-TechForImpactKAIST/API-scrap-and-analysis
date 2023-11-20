# coding=utf-8
# Source : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000897
import requests
from configurations.secrets import OpenDataPortalSecrets
import xml.etree.ElementTree as ET
import argparse

from . import SG_TYPECODE


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--code", action="store_true", help="코드를 출력합니다.")
args = parser.parse_args()
if args.code:
    formatted_code = ", ".join([f"({k}) {v}" for k, v in SG_TYPECODE.items()])
    print(formatted_code)
print("sgTypecode를 입력하면 해당 sgTypecode와 일치하는 sgId 값을 출력합니다. 여러 개를 입력하려면 ','로 구분해 주세요.")

url = "http://apis.data.go.kr/9760000/CommonCodeService/getCommonSgCodeList"
params = {
    "serviceKey": OpenDataPortalSecrets.service_key,
    "pageNo": "1",
    "numOfRows": "1000",
}

response = requests.get(url, params=params)
xml_data = response.content.decode("utf-8")
# Parse the XML data
root = ET.fromstring(xml_data)
# Find all elements where sgTypecode is equal to INPUT and extract their sgId values
sgIds = set()
for code in input("Input the number of sgTypecode: ").split(","):
    for item in root.findall(f'.//item[sgTypecode="{code}"]'):
        sgId_element = item.find("sgId")
        if sgId_element is not None:
            sgId = sgId_element.text
            sgIds.add(sgId)

# Print the sgId values
for sgId in sorted(sgIds):
    print(sgId)
