from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import requests


def scrap_sanchung(
    url="https://www.sancheong.go.kr/council/selectPersonalAssembly.do?key=2224&assemCate=8",
) -> ScrapResult:
    """산청군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find("ul", class_="comment_list")
    lis = mlist.find_all("li", recursive=False)
    for profile in lis:
        print(profile)
        info = profile.find_all("li")
        name = (
            profile.find("span", class_="name").get_text(strip=True)
            if profile.find("span", class_="name").get_text(strip=True)
            else "이름 정보 없음"
        )
        party = "정당 정보 없음"

        party_dd = info[3].get_text(strip=True).replace("소속정당", "")
        if party_dd:
            party = party_dd
        councilors.append(Councilor(name=name, jdName=party))

    return ScrapResult(
        council_id="hapchun",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_sanchung())
