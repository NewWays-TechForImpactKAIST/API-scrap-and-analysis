import os

from scrap.utils.requests import get_selenium, By
from scrap.local_councils import *
from scrap.local_councils.basic import find, findall

def scrap_26(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 중구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(find(soup, "div", class_="bbs_blog council"), "dl"):
        name_tag = profile.find_next("dt")
        name = (
            name_tag.get_text(strip=True).split()[-1].strip()
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find_next("li")
        if party_info:
            party = party_info.get_text(strip=True)[3:]

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_27(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 서구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in findall(soup, "div", class_="intro"):
        name_tag = profile.find_next("span").find_next("span")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_link = profile.find("a")
        if profile_link:
            profile_url = base_url + "/council" + profile_link["href"]
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find("span", string="소속정당")
            if party_info and (party_span := party_info.parent) is not None:
                party = party_span.text[4:].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_28(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 동구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="council_box"):
        name_tag = profile.find_next("span", class_="n2")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find_next("span", class_="n1")
        if party_info:
            party = party_info.get_text(strip=True).split("(")[1][:-1].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_29(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 영도구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="even-grid gap3pct panel1 p01205bg"):
        name_tag = profile.find_next("strong", class_="h1 title")
        name = (
            name_tag.get_text(strip=True).split(" ")[0].strip()
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_30(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 부산진구"""
    soup = get_soup(url, verify=False).find("ul", class_="mlist")
    councilors: list[Councilor] = []

    for profile in findall(soup, "dl"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find_all("b")[2]
        if party_info:
            party = party_info.find_next("span", class_="itemContent").get_text(
                strip=True
            )

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_31(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 동래구"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for name_tag in findall(soup, "li", class_="name"):
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = name_tag.find_next("li").find_next("li")
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_32(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 남구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(soup, "dl", class_="profile"):
        name_tag = profile.find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", class_="sbj", string="정   당")
        if party_info:
            party = (
                party_info.find_next("span", class_="detail")
                .get_text(strip=True)
                .split()[-1]
                .strip()
            )

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_33(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 북구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(soup, "dl", class_="info"):
        name_tag = profile.find("span")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", string="소속정당")
        if party_info:
            party = party_info.parent.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_34(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 해운대구"""
    soup = get_soup(url, verify=False).find("div", class_="initial_list")
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for name_tag in findall(soup, "dd"):
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        # 프로필보기 링크 가져오기
        profile_link = name_tag.find("a")
        assert profile_link is not None
        profile_url = base_url + profile_link["href"]
        profile_soup = get_soup(profile_url, verify=False)

        party_info = profile_soup.find("span", string="소속정당")
        party = ""
        if party_info and (party_span := party_info.parent) is not None:
            party = party_span.text[4:].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_35(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 기장군"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in findall(soup, "ul", class_="wulli bul02"):
        li_tags = profile.find_all("li")

        name_tag = li_tags[0]
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = li_tags[2]
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_36(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 사하구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for district_tag in findall(soup, "div", class_="list_member"):
        for name_tag in district_tag.find_all("h4", class_="name"):
            name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

            party = "정당 정보 없음"
            party_info = name_tag.find_next("span", string="소속당  : ")
            if party_info:
                party = party_info.parent.get_text(strip=True)[7:].strip()

            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_37(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 금정구"""
    soup = get_soup(url, verify=False).find("div", class_="council_list")
    councilors: list[Councilor] = []

    for profile in findall(soup, "a"):
        name_tag = profile.find("span", class_="tit").find("span")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        profile_url = profile["href"][:65] + "1" + profile["href"][66:]
        profile_soup = get_soup(profile_url, verify=False)

        party_info = profile_soup.find("span", class_="name", string="정당")
        party = ""
        if party_info and (party_span := party_info.parent) is not None:
            party = party_span.text[2:].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_38(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 강서구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile_img in findall(soup, "button", class_="btn_close"):
        profile = profile_img.find_next("dl")

        name_tag = profile.find("dd", class_="name")
        name = (
            name_tag.get_text(strip=True).split()[0].strip() if name_tag else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("span", class_="bold", string="정당 : ")
        if party_info:
            party = party_info.parent.get_text(strip=True)[5:].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_39(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 연제구"""
    councilors: list[Councilor] = []

    browser = get_selenium(url)

    councilor_infos = browser.find_elements(By.CSS_SELECTOR, "dl[class='info']")
    cur_win = browser.current_window_handle

    for info in councilor_infos:
        name_tag = info.find_element(By.TAG_NAME, "span")
        name = name_tag.text.strip() if name_tag else "이름 정보 없음"

        homepage_link = info.find_element(By.TAG_NAME, "a")
        homepage_link.click()
        browser.switch_to.window(
            [win for win in browser.window_handles if win != cur_win][0]
        )

        party_tag = browser.find_element(By.TAG_NAME, "tbody").find_elements(
            By.TAG_NAME, "td"
        )[3]
        party = party_tag.text.strip() if party_tag else "정당 정보 없음"

        browser.close()
        browser.switch_to.window(cur_win)

        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_40(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 수영구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="mem_info"):
        name_tag = profile.find("span", class_="name").find("span")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", string="소속정당 :")
        if party_info:
            party = party_info.parent.get_text(strip=True)[6:].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_41(url, cid, args: ArgsType = None) -> ScrapResult:
    """부산 사상구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for district in findall(soup, "ul", class_="council_list"):
        for profile in district.find_all("li"):
            name_tag = profile.find("span", class_="tit")
            name = (
                name_tag.get_text(strip=True).split()[0].strip()
                if name_tag
                else "이름 정보 없음"
            )

            party = "정당 정보 없음"
            party_info = profile.find("span", class_="con")
            if party_info:
                party = party_info.get_text(strip=True).split("]")[0].strip()[1:]

            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)