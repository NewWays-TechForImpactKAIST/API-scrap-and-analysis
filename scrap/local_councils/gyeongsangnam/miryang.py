from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup


def scrap_miryang(
    url="https://council.miryang.go.kr/web/EgovCouncilManList.do?menuNo=14010100",
) -> ScrapResult:
    """밀양시 의회 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("div", class_="council_box"):
        name_tag = (
            profile.find("span", string="이름").find_next("span").get_text(strip=True)
        )
        name = name_tag if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = (
            profile.find("span", string="소속정당").find_next("span").get_text(strip=True)
        )
        if party_info:
            party = party_info
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="miryang",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_miryang())
