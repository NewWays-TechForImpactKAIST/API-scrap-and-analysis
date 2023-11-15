"""
서울특별시 기초의회를 스크랩합니다. (1~25)
"""
from urllib.parse import urlparse

from scrap.local_councils import *


def scrap_1(url, cid, args: ArgsType = None
) -> ScrapResult:
    """서울 종로구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="pop_profile"):
        info = profile.find("div", class_="info")
        data_ul = info.find("ul", class_="detail")
        data_lis = data_ul.find_all("li")
        name = data_lis[0].find("span").get_text(strip=True)
        party = data_lis[2].find("span").get_text(strip=True)
        name = name if name else "이름 정보 없음"
        party = party if party else "정당 정보 없음"

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_2(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 중구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_3(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 용산구"""

    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_4(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 성동구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl", class_="profile"):
        name_tag = profile.find("strong", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("strong", string="정  당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_5(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 광진구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_6(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 동대문구"""
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
                profile_string = profile_info.get_text().strip().split(" ")
                idx = profile_string.index("소속정당")
                party = profile_string[idx + 2]

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_7(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 중랑구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_8(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 성북구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_9(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 강북구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_10(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 도봉구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_11(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 노원구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_12(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 은평구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_13(
    url, cid, args: ArgsType = None
) -> ScrapResult:
    """서울 서대문구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_14(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 마포구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="wrap"):
        name_tag = profile.find_next("div", class_="right")
        name = name_tag.find_next("h4").get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", class_="tit", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span", class_="con").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_15(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 양천구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_16(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 강서구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_17(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 구로구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_18(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 금천구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_19(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 영등포구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_20(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 동작구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_21(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 관악구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_22(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 서초구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_23(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 강남구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_24(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 송파구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find_next("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_25(url, cid, args: ArgsType = None) -> ScrapResult:
    """서울 강동구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


if __name__ == "__main__":
    print(scrap_24())
