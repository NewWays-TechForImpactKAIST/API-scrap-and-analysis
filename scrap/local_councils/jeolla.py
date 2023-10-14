from urllib.parse import urlparse

from scrap.utils.types import CouncilType, Councilor, ScrapResult, ScrapBasicArgument
from scrap.utils.requests import get_soup
from scrap.local_councils.basic import *


def scrap_154(
    url="https://council.namwon.go.kr/member/member.php",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 남원시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("ul", class_="info"):
        name_tag = profile.find("span", class_="name")
        name = name_tag.get_text(strip=True).split()[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(154),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_155(
    url="https://council.gimje.go.kr/index.gimje?menuCd=DOM_000000102001001000",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 김제시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="bbs_member"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(155),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_156(
    url="https://council.wanju.go.kr/board?depth_1=10&depth_2=33",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 완주군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []
    memberlist = soup.find("div", class_="card-member")

    for profile in memberlist.find_all("li"):
        name_tag = profile.find("div", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(156),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_157(
    url="https://council.jinan.go.kr/main2011/member/active.html",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 진안군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(157),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_160(
    url="https://council.imsil.go.kr/main/contents/lawmakerDistrict",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 임실군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    # TODO: js로 동적으로 읽어옴
    raise NotImplementedError

    return ScrapResult(
        council_id=str(160),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=[],
    )


def scrap_161(
    url="https://www.sunchangcouncil.go.kr/main/contents/lawmaker",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 순창군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    # TODO: js로 동적으로 읽어옴
    raise NotImplementedError

    return ScrapResult(
        council_id=str(161),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=[],
    )


def scrap_162(
    url="https://www.gochang.go.kr/council/index.gochang?menuCd=DOM_000000603005000000",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 고창군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="con_mem"):
        name_tag = profile.find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(157),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_163(
    url="https://council.buan.go.kr/index.buan?menuCd=DOM_000000104001002000",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 부안군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    profiles = soup.find_all("div", class_="person")
    profiles = profiles[1:]  # 첫 번째 태그는 홈페이지 목록

    for profile in profiles:
        name_tag = profile.find("p", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_tags = profile.find_all("li")
        for party_tag in party_tags:
            if "소속정당" in party_tag.text:
                party = party_tag.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(163),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_164(
    url="https://council.mokpo.go.kr/kr/member/active",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라남도 목포시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    base_url = "https://council.mokpo.go.kr/"
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name").get_text(strip=True)
        name = name_tag if name_tag else "이름 정보 없음"
        name = name.split("(")[0]  # 괄호 안에 있는 한자는 제외

        member_link = profile.find("a", class_="start")["href"]
        member_soup = get_soup(base_url + member_link)

        party_tag = member_soup.find("ul", class_="profile_list")
        party = (
            party_tag.select_one("li:contains('정 당')").text.replace("정 당:", "").strip()
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(164),
        council_type=CouncilType.LOCAL_COUNCIL.value,
        councilors=councilors,
    )


def scrap_165(
    url="https://council.yeosu.go.kr/source/korean/member/active.html",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라남도 여수시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("li", class_="name").get_text(strip=True)
        name = name_tag if name_tag else "이름 정보 없음"
        name = name.split("(")[0]  # 괄호 안에 있는 한자는 제외

        party_tag = [li for li in soup.find_all("li") if "소속정당" in li.get_text()]
        party = party_tag[0].get_text() if party_tag else "정당 정보 없음"

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(165),
        council_type=CouncilType.LOCAL_COUNCIL.value,
        councilors=councilors,
    )


def scrap_167(
    url="https://council.naju.go.kr/source/korean/member/active.html",
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 나주시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(167),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_167())
