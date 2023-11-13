# coding=utf-8
# Source : https://www.data.go.kr/data/15000864/openapi.do#/tab_layer_detail_function
import requests
import xml.etree.ElementTree as ET
from typing import List

from configurations.secrets import OpenDataPortalSecrets
from .utils import save_to_excel


BASE_URL = "http://apis.data.go.kr/9760000/WinnerInfoInqireService2/getWinnerInfoInqire"


def fetch_data(sgId: str, sgTypecode: str, page_no: int = 1, num_of_rows: int = 10_000) -> List[dict]:
    params = {
        "serviceKey": OpenDataPortalSecrets.service_key,
        "pageNo": str(page_no),
        "numOfRows": str(num_of_rows),
        "sgId": str(sgId),
        "sgTypecode": str(sgTypecode),
        "sggName": "",
        "sdName": "",
        "jdName": "",
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Error: Unable to fetch data for page {page_no}")
        return []

    root = ET.fromstring(response.content)

    data_list = []
    for item in root.findall(".//item"):
        data_entry = {child.tag: child.text for child in item}
        data_list.append(data_entry)

    return data_list


def fetch_all_data(sgIds: List[str], sgTypecode: str) -> List[dict]:
    data_list = []
    for sgId in sgIds:
        data_list.extend(fetch_data(sgId, sgTypecode))

    return data_list


if __name__ == "__main__":
    sgTypecode: str = input("원하는 sgTypecode 하나를 입력하세요:\n")
    sgIds: List[str] = input("원하는 sgId를 입력하세요. 여러 개라면 ','로 구분하여 입력하세요:\n").split(",")

    data_list = fetch_all_data(sgIds, sgTypecode)
    save_to_excel(data_list, sgTypecode, is_elected=True)
