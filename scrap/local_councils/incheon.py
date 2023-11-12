"""인천광역시를 스크랩. 50-57번째 의회까지 있음.
"""
from scrap.utils.requests import get_selenium, By
from scrap.local_councils.basic import (
    get_profiles,
    get_name,
    find,
    extract_party,
)
from scrap.local_councils import *


def scrap_50(url, cid) -> ScrapResult:
    """인천 중구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for name_tag in soup.find_all("p", class_="name"):
        name_tag_str = name_tag.get_text(strip=True).split("[")
        name = name_tag_str[0].strip()
        party = name_tag_str[-1][:-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_51(url, cid) -> ScrapResult:
    """인천 동구"""
    browser = get_selenium(url)
    councilors: list[Councilor] = []

    cur_win = browser.current_window_handle

    for profile in browser.find_elements(By.CSS_SELECTOR, "dl[class='profile']"):
        name_tag = profile.find_element(By.CSS_SELECTOR, "strong[class='name']")
        name = name_tag.text.strip() if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        profile_link = profile.find_element(By.TAG_NAME, "a")
        if profile_link:
            profile_link.click()
            browser.switch_to.window(
                [win for win in browser.window_handles if win != cur_win][0]
            )
            party_tag = browser.find_elements(By.CSS_SELECTOR, "span[class='detail']")[
                1
            ]
            if party_tag:
                party = party_tag.text.strip()

        councilors.append(Councilor(name, party))

        browser.close()
        browser.switch_to.window(cur_win)

    return ret_local_councilors(cid, councilors)


def scrap_52(url, cid) -> ScrapResult:
    """인천 미추홀구"""

    councilors: list[Councilor] = []
    browser = get_selenium(url)

    for profile in browser.find_elements(By.CSS_SELECTOR, "div[class='career_item']"):
        name_tag = profile.find_element(
            By.CSS_SELECTOR, "div[class='career_item_name']"
        )
        name = name_tag.text.strip().split()[0].strip() if name_tag else "이름 정보 없음"

        party_tag = profile.find_element(By.TAG_NAME, "dl")
        party = (
            party_tag.find_element(By.TAG_NAME, "dd").text.strip()
            if party_tag
            else "정당 정보 없음"
        )

        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_53(url, cid) -> ScrapResult:
    """인천 연수구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = (
            profile.find("em", string="소속정당").find_next("span").find_next("span")
        )
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_54(url, cid) -> ScrapResult:
    """인천 남동구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="정    당 : ").find_next("span")
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_55(url, cid) -> ScrapResult:
    """인천 부평구"""
    browser = get_selenium(url)
    councilors: list[Councilor] = []

    for profile in browser.find_elements(By.CSS_SELECTOR, "dl[class='profile']"):
        name_tag = profile.find_element(By.CSS_SELECTOR, "strong[class='name']")
        name = name_tag.text.strip().split()[0].strip() if name_tag else "이름 정보 없음"

        party_tag = profile.find_elements(By.TAG_NAME, "li")[2]
        party = (
            party_tag.find_element(By.TAG_NAME, "span").text.strip().split()[-1].strip()
            if party_tag
            else "정당 정보 없음"
        )
        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_56(url, cid) -> ScrapResult:
    """인천 계양구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for name_tag in soup.find_all("li", class_="name"):
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = (
            name_tag.find_next("li").find_next("li").find("span", class_="span_sfont")
        )
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_57(url, args) -> ScrapResult:
    """인천 서구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []
    cid = 57

    profiles = get_profiles(
        soup, args.pf_elt, args.pf_cls, args.pf_memlistelt, args.pf_memlistcls
    )
    print(cid, "번째 의회에는,", len(profiles), "명의 의원이 있습니다.")  # 디버깅용.

    for profile in profiles:
        name = get_name(
            profile, args.name_elt, args.name_cls, args.name_wrapelt, args.name_wrapcls
        )

        party = "정당 정보 없음"
        party_pulp = find(profile, args.pty_elt, class_=args.pty_cls)
        if party_pulp is None:
            raise AssertionError("[incheon.py] 정당정보 실패")
        party_string = party_pulp.get_text(strip=True)
        party_string = party_string.split(" ")[-1].strip()
        while True:
            party = extract_party(party_string)
            if party is not None:
                break
            if (party_pulp := party_pulp.find_next("span")) is not None:
                party_string = party_pulp.text.split(" ")[-1]
            else:
                raise RuntimeError("[incheon.py] 정당 정보 파싱 불가")

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


if __name__ == "__main__":
    print(scrap_51("https://council.icdonggu.go.kr/korean/member/active", 51))
