from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
from bs4 import BeautifulSoup


def scrap_yongsangu(url="https://www.yscl.go.kr/kr/member/name.do") -> ScrapResult:
    """
    Scrap councilors’ details from Yongsan-gu District Council of Seoul page.

    :param url: Yongsan-gu District Council members' list site url
    :return: Councilors’ name and party data in ScrapResult object
    """

    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-yongsangu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_yongsangu())
