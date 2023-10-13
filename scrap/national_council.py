import os
import json
from scrap.utils.types import CouncilType, Councilor, ScrapResult
import requests
import xml.etree.ElementTree as ET

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)


def scrap_national_council(cd: int) -> ScrapResult:
    """열린국회정보 Open API를 이용해 역대 국회의원 인적사항 스크랩
    _data 폴더에 assembly_api_key.json 파일을 만들어야 하며,
    해당 JSON은 {"key":"(Open API에서 발급받은 인증키)"} 꼴을 가져야 한다.
    https://open.assembly.go.kr/portal/data/service/selectAPIServicePage.do/OBL7NF0011935G18076#none

    :param cd: 국회의원 대수. 제20대 국회의원을 스크랩하고자 하면 20
    :return: 국회의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    key_json_path = os.path.join(BASE_DIR, "_data", "assembly_api_key.json")
    if not os.path.exists(key_json_path):
        raise Exception(
            "열린국회정보 Open API에 회원가입 후 인증키를 발급받아주세요.\nhttps://open.assembly.go.kr/portal/openapi/openApiDevPage.do"
        )
    with open(key_json_path, "r") as key_json:
        assembly_key = json.load(key_json)["key"]

    request_url = f"https://open.assembly.go.kr/portal/openapi/npffdutiapkzbfyvr?KEY={assembly_key}&UNIT_CD={cd + 100000}"
    response = requests.get(request_url)

    if response.status_code != 200:
        raise Exception(f"Open API 요청에 실패했습니다 (상태 코드 {response.status_code})")

    root = ET.fromstring(response.text)
    councilors: list[Councilor] = []

    for row in root.iter("row"):
        councilors.append(
            Councilor(name=row.find("HG_NM").text, party=row.find("POLY_NM").text)
        )

    return ScrapResult(
        council_id="national",
        council_type=CouncilType.NATIONAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_national_council(20))
