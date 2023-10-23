from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re


def scrap_65(url="https://council.donggu.go.kr/kr/member/active") -> ScrapResult:
    """대전시 동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in soup.find_all("dl", class_="profile"):
        name_tag = profile.find("strong", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_link = profile.find("a", class_="start")
        if profile_link:
            data_uid = profile_link.get("data-uid")
            if data_uid:
                profile_url = base_url + f"/kr/member/profile_popup?uid={data_uid}"
                profile_soup = get_soup(profile_url, verify=False)
                party_info = profile_soup.find("strong", string="정      당")
                if (
                    party_info
                    and (party_span := party_info.find_next("span")) is not None
                ):
                    party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-donggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_66(url="https://council.djjunggu.go.kr/kr/member/name.do") -> ScrapResult:
    """대전시 중구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-junggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_67(
    url="https://www.seogucouncil.daejeon.kr/svc/mbr/MbrPresent.do",
) -> ScrapResult:
    """대전시 서구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("dl"):
        name_tag = profile.find("dd", class_="name")
        name = (
            name_tag.get_text(strip=True).replace(" 의원", "") if name_tag else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = list(filter(lambda x: "정당" in str(x), profile.find_all("dd")))
        if party_info:
            party = party_info[0].get_text(strip=True).replace("정당: ", "")

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-seogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_68(url="https://yuseonggucouncil.go.kr/page/page02_01_01.php") -> ScrapResult:
    """대전시 유성구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        # () 안에 있는 한자를 제거 (ex. 김영희(金英姬) -> 김영희)
        name = name_tag.get_text(strip=True).split("(")[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        regex_pattern = re.compile(r"정\s*당\s*:", re.IGNORECASE)  # Case-insensitive
        party_info = profile.find("em", string=regex_pattern)
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-yuseonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_69(url="https://council.daedeok.go.kr/kr/member/name.do") -> ScrapResult:
    """대전시 대덕구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        regex_pattern = re.compile(r"정\s*당\s*:", re.IGNORECASE)  # Case-insensitive
        party_info = profile.find("em", string=regex_pattern)
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-daedeokgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_69())
