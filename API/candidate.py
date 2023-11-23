# coding=utf-8
# Source : https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15000908
import os, requests, sys
import xml.etree.ElementTree as ET
from typing import List
import argparse

from configurations.secrets import OpenDataPortalSecrets
from .utils import save_to_excel, save_to_mongo, getLocalMetroMap
from . import SG_TYPECODE, CANDIDATE_TYPECODE_TYPE


BASE_URL = "http://apis.data.go.kr/9760000/PofelcddInfoInqireService/getPofelcddRegistSttusInfoInqire"


def fetch_data(
    sgId: str,
    sgTypecode: str,
    drop_columns: List[str],
    page_no: int = 1,
    num_of_rows: int = 10_000,
) -> List[dict]:
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

        for column in drop_columns:
            data_entry.pop(column)

        data_list.append(data_entry)

    return data_list


def fetch_all_data(
    sgIds: List[str], sgTypecode: str, drop_columns: List[str]
) -> List[dict]:
    data_list = []
    for sgId in sgIds:
        data_list.extend(fetch_data(sgId, sgTypecode, drop_columns=drop_columns))

    return data_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="공공데이터포털 API로부터 후보자 정보를 가져옵니다.")
    parser.add_argument("sgTypecode", type=str, help="원하는 sgTypecode 하나를 입력하세요")
    parser.add_argument("sgIds", type=str, help="원하는 sgId를 ','로 구분하여 입력하세요")
    parser.add_argument(
        "--drop-columns",
        type=str,
        default="num,huboid,hanjaName,status",
        help="제거할 열 이름을 ','로 구분하여 입력하세요",
    )
    parser.add_argument(
        "--save-method",
        type=str,
        # TODO: Add MongoDB support
        # choices=["excel", "mongo"],
        choices=["excel"],
        default="excel",
        help="데이터 저장 방식: 'excel' (현재는 excel만 지원)",
    )

    args = parser.parse_args()
    sgIds = args.sgIds.split(",")
    drop_columns = args.drop_columns.split(",") if args.drop_columns else []

    data_list = fetch_all_data(sgIds, args.sgTypecode, drop_columns=drop_columns)

    if args.save_method == "excel":
        save_to_excel(data_list, args.sgTypecode, is_elected=False)
    elif args.save_method == "mongo":
        save_to_mongo(
            data_list, args.sgTypecode, CANDIDATE_TYPECODE_TYPE[args.sgTypecode]
        )
