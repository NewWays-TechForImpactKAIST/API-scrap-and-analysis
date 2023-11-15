from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup

import re


def scrap_sangju(
    url="https://www.sangjucouncil.go.kr/kr/member/name.do",
) -> ScrapResult:
    """대전시 동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name").find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ScrapResult(
        council_id="sangju",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_sangju())
