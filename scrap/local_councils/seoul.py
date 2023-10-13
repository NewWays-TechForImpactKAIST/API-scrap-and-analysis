from urllib.parse import urlparse
import re

from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup


def scrap_1(
    url="https://council.jongno.go.kr/council/councilAsemby/list/estList.do?menuNo=400021",
) -> ScrapResult:
    """서울시 종로구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="chairman-info"):
        name_tag = profile.find_next("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-junggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_2(url="https://02jgnew.council.or.kr/kr/member/active") -> ScrapResult:
    """서울시 중구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    parliment_soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in parliment_soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_link = profile.find("a", class_="start")
        if profile_link:
            profile_url = base_url + profile_link["href"]
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find("em", string="소속정당 : ")
            if party_info and (party_span := party_info.find_next("span")) is not None:
                party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-junggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_3(url="https://www.yscl.go.kr/kr/member/name.do") -> ScrapResult:
    """서울시 용산구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

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


def scrap_4(url="https://sdcouncil.sd.go.kr/kr/member/active2") -> ScrapResult:
    """서울시 성동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl", class_="profile"):
        name_tag = profile.find("strong", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("strong", string="정  당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-seongdonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_5(url="https://council.gwangjin.go.kr/kr/member/active") -> ScrapResult:
    """서울시 광진구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all(
        "div", class_=lambda x: x in ("profile", "profile_none")
    ):
        name_tag = profile.find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-gwangjingu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_6(url="http://council.ddm.go.kr/citizen/menu1.asp") -> ScrapResult:
    """서울시 동대문구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    parliment_soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in parliment_soup.find_all("div", class_="intro_text tm_lg_6"):
        name = profile.find("p", class_="intro_text_title").string.strip().split(" ")[0]
        party = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_link = profile.find("a")
        if profile_link:
            profile_url = (
                base_url
                + "/assemblyman/greeting/menu02.asp?assembly_id="
                + profile_link["href"][1:]
            )
            profile_soup = get_soup(profile_url, verify=False, encoding="euc-kr")

            profile_info = profile_soup.find("div", class_="profileTxt")
            if profile_info:
                profile_string = profile_info.get_text().strip().split("\xa0")
                idx = profile_string.index("소속정당")
                party = profile_string[idx + 2]

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-dongdaemungu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_7(url="https://council.jungnang.go.kr/kr/member/name2.do") -> ScrapResult:
    """서울시 중랑구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-jungnanggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_8(url="https://www.sbc.go.kr/kr/member/active.do") -> ScrapResult:
    """서울시 성북구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = (
                party_info.find_next("span").get_text(strip=True).split(" ")[-1].strip()
            )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-seongbukgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_9(url="https://council.gangbuk.go.kr/kr/member/name.do") -> ScrapResult:
    """서울시 강북구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name")
        name = (
            name_tag.find_next("strong").get_text(strip=True)
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-gangbukgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_10(
    url="https://www.council-dobong.seoul.kr/kr/member/active.do",
) -> ScrapResult:
    """서울시 도봉구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = (
                party_info.find_next("span").get_text(strip=True).split(" ")[-1].strip()
            )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-dobonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_11(url="https://council.nowon.kr/kr/member/active.do") -> ScrapResult:
    """서울시 노원구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = (
                party_info.find_next("span").get_text(strip=True).split(" ")[-1].strip()
            )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-nowongu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_12(url="https://council.ep.go.kr/kr/member/name.do") -> ScrapResult:
    """서울시 은평구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name")
        name = (
            name_tag.find_next("strong").get_text(strip=True)
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-eunpyeonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_13(
    url="https://www.sdmcouncil.go.kr/source/korean/square/ascending.html",
) -> ScrapResult:
    """서울시 서대문구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl", class_="card_desc"):
        name_tag = profile.find_next("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("ul")
        if party_info:
            party = (
                party_info.find_next("li")
                .find_next("li")
                .find_next("li")
                .get_text(strip=True)
                .split(" ")[-1]
                .strip()
            )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-seodaemungu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_14(url="https://council.mapo.seoul.kr/kr/member/active.do") -> ScrapResult:
    """서울시 마포구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="wrap"):
        name_tag = profile.find_next("div", class_="right")
        name = name_tag.find_next("h4").get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", class_="tit", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span", class_="con").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-mapogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_15(url="https://www.ycc.go.kr/kr/member/active") -> ScrapResult:
    """서울시 양천구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("div", class_="name")
        name = (
            name_tag.find_next("strong").get_text(strip=True)
            if name_tag
            else "이름 정보 없음"
        )
        party = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_uid = profile.find("a", class_="start")["data-uid"]
        if profile_uid:
            profile_url = base_url + "/kr/member/profile_popup?uid=" + profile_uid
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find("em", string="소속정당")
            if party_info and (party_span := party_info.find_next("span")):
                party = party_span.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-yangcheongu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_16(url="https://gsc.gangseo.seoul.kr/member/org.asp") -> ScrapResult:
    """서울시 강서구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("ul", class_="mb-15"):
        name_tag = profile.find_next("span", class_="fs-18 fw-700")
        name = (
            name_tag.get_text(strip=True).split()[0].strip() if name_tag else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = (
            profile.find_next("span", class_="title")
            .find_next("span", class_="title")
            .find_next("span", class_="title")
        )
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-gangseogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_17(url="https://www.guroc.go.kr/kr/member/name.do") -> ScrapResult:
    """서울시 구로구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("div", class_="name")
        name = (
            name_tag.find_next("strong").get_text(strip=True)
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-gurogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_18(url="https://council.geumcheon.go.kr/member/member.asp") -> ScrapResult:
    """서울시 금천구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("li", class_="name"):
        name_tag = profile.find_next("strong")
        name = (
            name_tag.get_text(strip=True).split("(")[0].strip()
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-geumcheongu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_19(url="https://www.ydpc.go.kr/kr/member/active.do") -> ScrapResult:
    """서울시 영등포구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-yeongdeungpogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_20(url="http://assembly.dongjak.go.kr/kr/member/name.do") -> ScrapResult:
    """서울시 동작구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-dongjakgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_21(url="https://www.ga21c.seoul.kr/kr/member/name.do") -> ScrapResult:
    """서울시 관악구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = (
                party_info.find_next("span").get_text(strip=True).split(" ")[-1].strip()
            )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-gwanakgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_22(url="https://www.sdc.seoul.kr/kr/member/active.do") -> ScrapResult:
    """서울시 서초구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("em", class_="name")
        name = (
            name_tag.get_text(strip=True).split()[0].strip() if name_tag else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-seochogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_23(url="https://www.gncouncil.go.kr/kr/member/name.do") -> ScrapResult:
    """서울시 강남구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("div", class_="name")
        name = (
            name_tag.find_next("strong").get_text(strip=True)
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-gangnamgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_24(url="https://council.songpa.go.kr/kr/member/active.do") -> ScrapResult:
    """서울시 송파구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    # TODO
    raise Exception("송파구 의회 사이트는 현재 먹통입니다")


def scrap_25(url="https://council.gangdong.go.kr/kr/member/active.do") -> ScrapResult:
    """서울시 강동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("em", class_="name")
        name = (
            name_tag.get_text(strip=True).split()[0].strip() if name_tag else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-gangdonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_2())
