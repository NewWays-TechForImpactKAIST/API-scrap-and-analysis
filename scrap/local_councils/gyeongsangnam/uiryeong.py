from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup


def scrap_uiryeong(
    url="https://www.uiryeong.go.kr/board/list.uiryeong?boardId=BBS_0000169&menuCd=DOM_000000502001000000&contentsSid=1040",
) -> ScrapResult:
    """
    Scrap councilors’ details from Yongsan-gu District Council of Seoul page.

    :param url: Yongsan-gu District Council members' list site url
    :return: Councilors’ name and party data in ScrapResult object
    """

    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("li", class_="assemList"):
        name_tag = profile.find("p", class_="assemName")
        name = name_tag.get_text(strip=True).split(" ")[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("ul", class_="assemCate")
        party_info = party_info.find("li")
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="goseong",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_uiryeong())
