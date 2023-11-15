from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re


def scrap_damyang(url="https://council.gc.go.kr/kr/member/active.do") -> ScrapResult:
    """담양군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="memlist")[0]

    for profile in mlist.find_all("li", recursive=False):
        info = profile.find("ul", class_="info")
        name = (
            info.find("h5").get_text(strip=True)
            if info.find("h5").get_text(strip=True)
            else "이름 정보 없음"
        )

        li = info.find("li", class_="item MP")
        party = "정당 정보 없음"
        party_dd = li.find_all("dd")[1]
        if party_dd:
            party = party_dd.get_text(strip=True)
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="damyang",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_damyang())
