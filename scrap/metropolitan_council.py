from urllib.parse import urlparse

from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup


def scrap_metro_1(
    url="https://www.smc.seoul.kr/main/memIntro01.do?menuId=001002001001",
) -> ScrapResult:
    """서울시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in soup.find_all("input", class_="memLinkk"):
        name = profile["value"].strip() if profile else "이름 정보 없음"
        party = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_url = base_url + "/home/" + profile["data-url"]
        profile_soup = get_soup(profile_url, verify=False)

        party_info = profile_soup.find("div", class_="profile")
        if party_info and (party_span := party_info.find("li")) is not None:
            party = party_span.find_next("li").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_2(url="https://council.busan.go.kr/council/past02") -> ScrapResult:
    """부산시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False).find("ul", class_="inmemList")
    councilors: list[Councilor] = []

    for profile in soup.find_all("a", class_="detail"):
        name = profile.get_text(strip=True) if profile else "이름 정보 없음"
        party = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_url = profile["href"]
        profile_soup = get_soup(profile_url, verify=False)

        party_info = profile_soup.find("ul", class_="vs-list-st-type01")
        if party_info and (party_span := party_info.find("li")) is not None:
            party = (
                party_span.find_next("li")
                .find_next("li")
                .get_text(strip=True)
                .split()[-1]
                .strip()
            )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_3(url="https://council.daegu.go.kr/kr/member/active") -> ScrapResult:
    """대구시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="pop_profile"):
        name_tag = profile.find("p", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daegu",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_4(url="https://www.icouncil.go.kr/main/member/name.jsp") -> ScrapResult:
    """인천시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False).find("table", class_="data").find("tbody")
    councilors: list[Councilor] = []

    for profile in soup.find_all("tr"):
        columns = profile.find_all("td")

        name_tag = columns[0]
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party_tag = columns[1]
        party = party_tag.get_text(strip=True) if party_tag else "정당 정보 없음"

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="incheon",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_5(url="https://council.gwangju.go.kr/index.do?PID=029") -> ScrapResult:
    """광주시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False).find("table", class_="data").find("tbody")
    councilors: list[Councilor] = []

    # TODO

    return ScrapResult(
        council_id="gwangju",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_6(
    url="https://council.daejeon.go.kr/svc/cmp/MbrListByPhoto.do",
) -> ScrapResult:
    """대전시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False).find("ul", class_="mlist")
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.find("strong").get_text(strip=True) if name_tag else "이름 정보 없음"

        party_tag = name_tag.find_next("dd").find_next("dd")
        party = party_tag.find("i").get_text(strip=True) if party_tag else "정당 정보 없음"

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_7(
    url="https://www.council.ulsan.kr/kor/councillor/viewByPerson.do",
) -> ScrapResult:
    """울산시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for name_tag in soup.find_all("div", class_="name"):
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party_tag = name_tag.find_next("li").find_next("li")
        party = party_tag.get_text(strip=True) if party_tag else "정당 정보 없음"

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="ulsan",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_8(
    url="https://council.sejong.go.kr/mnu/pom/introductionMemberByName.do",
) -> ScrapResult:
    """세종시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False).find("ul", class_="ml")
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl"):
        name_tag = profile.find("dd", class_="name")
        name = (
            name_tag.find(string=True, recursive=False).strip()
            if name_tag
            else "이름 정보 없음"
        )

        party_tag = name_tag.find_next("dd").find_next("dd")
        party = (
            party_tag.get_text(strip=True).split()[-1].strip()
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="sejong",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_9(
    url="https://www.ggc.go.kr/site/main/memberInfo/actvMmbr/list?cp=1&menu=consonant&sortOrder=MI_NAME&sortDirection=ASC",
) -> ScrapResult:
    """경기도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False).find("div", class_="paging2 clearfix")
    councilors: list[Councilor] = []

    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for page in soup.find_all("a"):
        page_url = base_url + page["href"]
        page_soup = get_soup(page_url, verify=False).find(
            "ul", class_="memberList3 clear"
        )
        for profile in page_soup.find_all("li", recursive=False):
            name_tag = profile.find("p", class_="f22 blue3")
            name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

            party_tag = profile.find("li", class_="f15 m0")
            party = party_tag.get_text(strip=True) if party_tag else "정당 정보 없음"

            councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="gyeonggi",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_10(
    url="https://council.chungbuk.kr/kr/member/active.do",
) -> ScrapResult:
    """충청북도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = (
            name_tag.get_text(strip=True).split()[0].strip() if name_tag else "이름 정보 없음"
        )

        party_tag = profile.find("em", string="소속정당")
        party = (
            party_tag.find_next("span").find_next("span").get_text(strip=True)
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="chungbuk",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_11(
    url="https://council.chungnam.go.kr/kr/member/name.do",
) -> ScrapResult:
    """충청남도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = (
            name_tag.get_text(strip=True).split()[0].strip() if name_tag else "이름 정보 없음"
        )

        party_tag = profile.find("em", string="소속정당 : ")
        party = (
            party_tag.find_next("span").get_text(strip=True)
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="chungnam",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_12(
    url="https://www.assem.jeonbuk.kr/board/list.do?boardId=2018_assemblyman&searchType=assem_check&keyword=1&menuCd=DOM_000000103001000000&contentsSid=453",
) -> ScrapResult:
    """전라북도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("li", class_="career"):
        name_tag = profile.find("tr", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party_tag = profile.find("tr", class_="list1")
        party = (
            party_tag.find("td", class_="co2").get_text(strip=True)
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="jeonbuk",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_13(
    url="https://www.jnassembly.go.kr/profileHistory.es?mid=a10202010000&cs_daesoo=12",
) -> ScrapResult:
    """전라남도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("tbody"):
        name_tag = profile.find("p")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party_tag = profile.find("th", string="소속정당")
        party = (
            party_tag.find_next("td", class_="txt_left").get_text(strip=True)
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="jeonnam",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_14(url="https://council.gb.go.kr/kr/member/name") -> ScrapResult:
    """경상북도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name")
        name = name_tag.find("strong").get_text(strip=True) if name_tag else "이름 정보 없음"

        party_tag = profile.find("em", string="소속정당")
        party = (
            party_tag.find_next("span").find_next("span").get_text(strip=True)
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="gyeongbuk",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_15(
    url="https://council.gyeongnam.go.kr/kr/member/active.do",
) -> ScrapResult:
    """경상남도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name")
        name = (
            name_tag.find("strong").get_text(strip=True).split("(")[0].strip()
            if name_tag
            else "이름 정보 없음"
        )

        party_tag = profile.find("em", class_="ls2", string="정당")
        party = (
            party_tag.find_next("span").get_text(strip=True)
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="gyeongnam",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_16(url="https://council.gangwon.kr/kr/member/name.do") -> ScrapResult:
    """강원도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party_tag = profile.find("em", string="소속정당")
        party = (
            party_tag.find_next("span").get_text(strip=True).split()[-1].strip()
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="gangwon",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


def scrap_metro_17(
    url="https://www.council.jeju.kr/cmember/active/name.do",
) -> ScrapResult:
    """제주도 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for tag in soup.find_all("p", class_="name"):
        text = tag.get_text(strip=True).split("(")
        # print(text)
        name = text[0].strip()
        party = text[1][:-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="jeju",
        council_type=CouncilType.METROPOLITAN_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_metro_17())
