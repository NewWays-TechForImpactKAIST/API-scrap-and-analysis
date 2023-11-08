"""인천광역시를 스크랩. 50-57번째 의회까지 있음.
"""
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup, get_selenium, By
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

    return returncouncilors(cid, councilors)


def scrap_51(url, cid) -> ScrapResult:
    """인천 동구"""
    raise Exception("현재 인천 동구의회 사이트는 SSLV3_ALERT_HANDSHAKE_FAILURE 에러가 발생합니다")

    # soup = get_soup(url, verify=False)
    # councilors: list[Councilor] = []


# # 프로필 링크 스크랩을 위해 base_url 추출
# parsed_url = urlparse(url)
# base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

# for name_tag in soup.find_all('strong', class_='name'):
#     name = name_tag.get_text(strip=True)
#     party = '정당 정보 없음'

#     profile_link = name_tag.find_next('a', class_='abtn1')
#     if profile_link:
#         profile_url = base_url + profile_link['onclick'][13:104]
#         profile_soup = get_soup(profile_url, verify=False)

#         party_info = profile_soup.find('span', class_='subject', string='소속정당')
#         if party_info and (party_span := party_info.find_next('span', class_='detail')) is not None:
#             party = party_span.get_text(strip=True)

#     councilors.append(Councilor(name=name, party=party))

# return returncouncilors(cid, councilors)


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

    return returncouncilors(cid, councilors)


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

    return returncouncilors(cid, councilors)


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

    return returncouncilors(cid, councilors)


def scrap_55(url, cid) -> ScrapResult:
    """인천 부평구"""
    raise Exception("현재 인천 부평구의회 사이트는 SSLV3_ALERT_HANDSHAKE_FAILURE 에러가 발생합니다")

    # soup = get_soup(url, verify=False)
    # councilors: list[Councilor] = []

    # for profile in soup.find_all('div', class_='profile'):
    #     name_tag = profile.find('strong', class_='name')
    #     name = name_tag.get_text(strip=True).split()[0].strip() if name_tag else '이름 정보 없음'

    #     party = '정당 정보 없음'
    #     party_info = profile.find('strong', string='소속정당').find_next('span')
    #     if party_info:
    #         party = party_info.get_text(strip=True).split()[-1].strip()

    #     councilors.append(Councilor(name=name, party=party))

    # return returncouncilors(cid, councilors)
    #     council_id=55,
    #     council_type=CouncilType.LOCAL_COUNCIL,
    #     councilors=councilors
    # )


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

    return returncouncilors(cid, councilors)


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

    return returncouncilors(cid, councilors)


if __name__ == "__main__":
    print(scrap_52())
