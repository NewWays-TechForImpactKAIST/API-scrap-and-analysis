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
    sgIds: List[str], sgTypecodes: str, drop_columns: List[str]
) -> List[dict]:
    data_list = []
    for sgTypecode in sgTypecodes.split(","):
        for sgId in sgIds:
            data_list.extend(fetch_data(sgId, sgTypecode, drop_columns=drop_columns))

    return data_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="공공데이터포털 API로부터 후보자 정보를 가져옵니다.")
    parser.add_argument("sgTypecodes", type=str, help="원하는 sgTypecode를 ','로 구분하여 입력하세요")
    parser.add_argument("sgIds", type=str, help="원하는 sgId를 ','로 구분하여 입력하세요")
    parser.add_argument(
        "--drop-columns",
        type=str,
        default="num,huboid,hanjaName,status,gihoSangse",
        help="제거할 열 이름을 ','로 구분하여 입력하세요",
    )
    parser.add_argument(
        "-m", "--update-mongo", help="API 요청 결과를 MongoDB에 업데이트", action="store_true"
    )
    parser.add_argument(
        "-o", "--output-store", help="API 요청 결과를 로컬에 저장", action="store_true"
    )
    parser.add_argument("--output-path", help="API 요청 결과 저장 경로", default="output")



    args = vars(parser.parse_args())
    print(args)
    sgIds = args.get("sgIds").split(",")
    if args.get("drop_columns"):
        drop_columns = args.get("drop_columns").split(",")
    else:
        drop_columns = []
    print(drop_columns)

    data_list = fetch_all_data(sgIds, args.get("sgTypecodes"), drop_columns=drop_columns)

    for sgTypecode in args.get("sgTypecodes").split(","):
        if sgTypecode not in SG_TYPECODE:
            raise ValueError(f"Invalid sgTypecode: {sgTypecode}")

        if args.get("update_mongo"):
            save_to_mongo(data_list, sgTypecode, CANDIDATE_TYPECODE_TYPE[sgTypecode])

        if args.get("output_store"):
            save_to_excel(data_list, sgTypecode, is_elected=False)