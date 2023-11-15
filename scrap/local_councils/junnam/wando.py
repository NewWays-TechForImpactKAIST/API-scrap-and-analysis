from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import requests


def scrap_wando(
    url="http://www.wdcc.or.kr:8088/common/selectCouncilMemberList.json?searchCsDaesoo=9",
) -> ScrapResult:
    """완도군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    councilors: List[Councilor] = []

    result = requests.get(url)
    result_json = result.json()
    for profile in result_json["list"]:
        name = profile["cmNm"]
        party = profile["mpParty"]
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="wando",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_wando())
