from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import requests


def scrap_chilgok(
    url="https://council.chilgok.go.kr/content/member/member.html",
) -> ScrapResult:
    """칠곡군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="memberUl")[0]

    for profile in mlist.find_all("li", recursive=False):
        info = profile.find_all("dd")
        if info:
            name = (
                profile.find("dd", class_="name").get_text(strip=True)
                if profile.find("dd", class_="name").get_text(strip=True)
                else "이름 정보 없음"
            )

            party = "정당 정보 없음"
            party_dd = info[3].get_text(strip=True).replace("정당 : ", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, jdName=party))

    return ScrapResult(
        council_id="chilgok",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_chilgok())
