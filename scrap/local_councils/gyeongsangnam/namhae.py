from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re


def scrap_namhae(
    url="https://council.namhae.go.kr/source/korean/member/active.html",
) -> ScrapResult:
    """남해 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("li", class_="name")
        name = name_tag.get_text(strip=True).split("(")[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find_all("li")[3]
        if party_info:
            party = party_info.get_text(strip=True).replace("소속정당 : ", "")
        councilors.append(Councilor(name=name, jdName=party))

    return ScrapResult(
        council_id="yangsan",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_namhae())
