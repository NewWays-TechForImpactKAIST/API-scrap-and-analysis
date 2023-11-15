from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import requests


def scrap_hanam(url="https://www.haman.go.kr/04646/04669.web") -> ScrapResult:
    """합천군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("div", class_="column")

    for profile in mlist:
        name = (
            profile.find("h2").get_text(strip=True).split("\n")[0]
            if profile.find("h2").get_text(strip=True)
            else "이름 정보 없음"
        )
        info = profile.find_all("li")
        if info:
            party = "정당 정보 없음"
            party_dd = info[2].get_text(strip=True).replace("정당", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="hanam",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_hanam())
