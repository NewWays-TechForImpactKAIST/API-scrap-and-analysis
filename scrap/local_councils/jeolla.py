import requests
from scrap.local_councils import *
from scrap.utils.requests import get_selenium, By
from scrap.local_councils.basic import (
    getprofiles,
    getname,
    extract_party,
    find,
    findall,
    sel_find,
    regex_pattern,
)

party_keywords = getPartyList()
party_keywords.append("무소속")

def scrap_154(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라북도 남원시"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in findall(soup, "ul", class_="info"):
        name_tag = profile.find("span", class_="name")
        name = name_tag.get_text(strip=True).split()[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_155(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라북도 김제시"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="bbs_member"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_156(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라북도 완주군"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []
    memberlist = soup.find("div", class_="card-member")

    for profile in findall(memberlist, "li"):
        name_tag = profile.find("div", class_="name")
        name = name_tag.get_text(strip=True).split()[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_157(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라북도 진안군"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="profile"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_160(url, cid, args: ArgsType = None) -> ScrapResult:
    """전라북도 임실군"""
    browser = get_selenium(url)
    councilors: list[Councilor] = []

    for profile in browser.find_elements(By.CSS_SELECTOR, "div[class='col-lg-6']"):
        name_tag = profile.find_element(By.TAG_NAME, "strong")
        name = name_tag.text.strip() if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_161(url, cid, args: ArgsType = None) -> ScrapResult:
    """전라북도 순창군"""
    browser = get_selenium(url)
    councilors: list[Councilor] = []

    for profile in browser.find_elements(By.CSS_SELECTOR, "div[class='con']"):
        name_tag = profile.find_element(By.TAG_NAME, "strong")
        name = name_tag.text.strip()[:-2].strip() if name_tag else "이름 정보 없음"

        party_tag = profile.find_elements(By.TAG_NAME, "dd")[1]
        party = party_tag.text.strip() if party_tag else "정당 정보 없음"

        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_162(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라북도 고창군"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="con_mem"):
        name_tag = profile.find("strong")
        name = name_tag.get_text(strip=True).split()[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_163(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라북도 부안군"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    profiles = findall(soup, "div", class_="person")
    profiles = profiles[1:]  # 첫 번째 태그는 홈페이지 목록

    for profile in profiles:
        name_tag = profile.find("p", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_tags = profile.find_all("li")
        for party_tag in party_tags:
            if "소속정당" in party_tag.text:
                party = party_tag.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_164(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라남도 목포시"""
    base_url = "https://council.mokpo.go.kr/"
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="profile"):
        name_tag = profile.find("em", class_="name").get_text(strip=True)
        name = name_tag if name_tag else "이름 정보 없음"
        name = name.split("(")[0]  # 괄호 안에 있는 한자는 제외

        member_link = profile.find("a", class_="start")["href"]
        member_soup = get_soup(base_url + member_link)

        party_tag = find(member_soup, "ul", class_="profile_list")
        party = (
            party_tag.select_one("li:contains('정 당')").text.replace("정 당:", "").strip()
        )

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_165(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라남도 여수시"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="profile"):
        name_tag = profile.find("li", class_="name").get_text(strip=True)
        name = name_tag if name_tag else "이름 정보 없음"
        name = name.split("(")[0]  # 괄호 안에 있는 한자는 제외

        party_tag = [li for li in findall(soup, "li") if "소속정당" in li.get_text()]
        party = party_tag[0].get_text() if party_tag else "정당 정보 없음"

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_167(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라북도 나주시"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in findall(soup, "div", class_="profile"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


# def goto_profilesite_171(profile, wrapper_element, wrapper_class_, wrapper_txt, url):
#     # 프로필보기 링크 가져오기
#     profile_link = find(profile, wrapper_element, class_=wrapper_class_)
#     if wrapper_txt is not None:
#         profile_links = find_all(profile, "a", class_=wrapper_class_)
#         profile_link = [link for link in profile_links if link.text == wrapper_txt][0]
#     if profile_link is None:
#         raise RuntimeError("[basic.py] 의원 프로필에서 프로필보기 링크를 가져오는데 실패했습니다.")
#     profile_url = profile_link["href"] + "/main/"
#     print(profile_url)
#     try:
#         profile = get_soup(profile_url, verify=False)
#     except Exception:
#         raise RuntimeError("[basic.py] '//'가 있진 않나요?", " url: ", profile_url)
#     return profile

# def get_party_171(
#     profile, element, class_, wrapper_element, wrapper_class_, wrapper_txt, url
# ):
#     # 의원 프로필에서 의원이 몸담는 정당 이름을 가져옴
#     if wrapper_element is not None:
#         profile = goto_profilesite_171(
#             profile, wrapper_element, wrapper_class_, wrapper_txt, url
#         )
#     print(profile.text)
#     print(find_all(profile, element, class_))
#     print("hihih")
#     party_pulp_list = list(
#         filter(
#             lambda x: regex_pattern.search(str(x)), find_all(profile, element, class_)
#         )
#     )
#     if party_pulp_list == []:
#         raise RuntimeError("[basic.py] 정당정보 regex 실패")
#     party_pulp = party_pulp_list[0]
#     party_string = party_pulp.get_text(strip=True).split(" ")[-1]
#     while True:
#         if (party := extract_party(party_string)) is not None:
#             return party
#         if (party_pulp := party_pulp.find_next("span")) is not None:
#             party_string = party_pulp.text.strip().split(" ")[-1]
#         else:
#             return "[basic.py] 정당 정보 파싱 불가"


# def scrap_171(
#     url,
#     cid,
#     args: ArgsType = None,
# ) -> ScrapResult:
#     """전라남도 곡성군"""
#     soup = get_soup(url, verify=False)
#     councilors: list[Councilor] = []

#     profiles = get_profiles(
#         soup, args.pf_elt, args.pf_cls, args.pf_memlistelt, args.pf_memlistcls
#     )
#     print(cid, "번째 의회에는,", len(profiles), "명의 의원이 있습니다.")  # 디버깅용.

#     for profile in profiles:
#         name = party = ""
#         try:
#             name = get_name(
#                 profile,
#                 args.name_elt,
#                 args.name_cls,
#                 args.name_wrapelt,
#                 args.name_wrapcls,
#             )
#         except Exception as e:
#             raise RuntimeError("[basic.py] 의원 이름을 가져오는데 실패했습니다. 이유 : " + str(e))
#         try:
#             party = get_party_171(
#                 profile,
#                 args.pty_cls,
#                 args.pty_elt,
#                 args.pty_wrapelt,
#                 args.pty_wrapcls,
#                 args.pty_wraptxt,
#                 url,
#             )
#         except Exception as e:
#             raise RuntimeError("[basic.py] 의원 정당을 가져오는데 실패했습니다. 이유: " + str(e))
#         councilors.append(Councilor(name=name, party=party))

#     return ret_local_councilors(cid, councilors)

def scrap_175(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라남도 화순군"""
    browser = get_selenium(url)
    councilors: list[Councilor] = []
    for profileList in browser.find_elements(By.CSS_SELECTOR, "ul[id='councilList']"):
        for profile in profileList.find_elements(By.CSS_SELECTOR, "ul[class='name_51']"):
            name_tag = profile.find_element(By.TAG_NAME, "li")
            name = name_tag.text.strip() if name_tag else "이름 정보 없음"

            profile_link = sel_find(profile, "a")
            page_content = get_selenium(profile_link.get_attribute("href")).page_source
            party = ""
            for keyword in party_keywords:
                if keyword in page_content:
                    party = keyword
                    break

            councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)

def scrap_177(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라남도 강진군"""
    browser = get_selenium(url)
    councilors: list[Councilor] = []
    for profileList in browser.find_elements(By.CSS_SELECTOR, "ul[id='memlist']"):
        for profile in profileList.find_elements(By.CSS_SELECTOR, "ul[class='info']"):
            name_tag = profile.find_element(By.TAG_NAME, "h5")
            name = name_tag.text.strip() if name_tag else "이름 정보 없음"
            party = ""
            for keyword in party_keywords:
                if keyword in profile.text:
                    party = keyword
                    break
            party = "정당 정보 없음"
            councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_178(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라남도 완도군"""
    browser = get_selenium(url)
    councilors: list[Councilor] = []
    for profileList in browser.find_elements(By.CSS_SELECTOR, "div[class='congressperson_list']"):
        for profile in profileList.find_elements(By.CSS_SELECTOR, "div[class='col-lg-6']"):
            name_tag = profile.find_element(By.TAG_NAME, "strong")
            name = name_tag.text.strip() if name_tag else "이름 정보 없음"
            profile_link = sel_find(profile, "a", class_="icon_btn")
            page_content = get_selenium(profile_link.get_attribute("href")).page_source
            party = ""
            for keyword in party_keywords:
                if keyword in page_content:
                    party = keyword
                    break
            councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_179(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="memberList")[0]

    for profile in mlist.find_all("li", recursive=False):
        name_tag = profile.find("h4")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        for keyword in party_keywords:
            if keyword in profile.text:
                party = keyword
                break
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_182(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라남도 강진군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="formerCouncillor")[0]

    for profile in mlist.find_all("li", recursive=False):
        info = profile.find("div", class_="profileInfo")
        name = (
            info.find("div", class_="infosubmem_name").get_text(strip=True)
            if info.find("div", class_="infosubmem_name").get_text(strip=True)
            else "이름 정보 없음"
        )

        party_dd = info.find("div", class_="infoContents")
        party = "정당 정보 없음"
        if party_dd:
            party = party_dd.get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_183(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라남도 영광군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("div", class_="councilors_curr2_wrap")[0]

    for profile in mlist.find_all("div", class_="subcon_body_txt", recursive=False):
        info = profile.find("div", class_="ygmember_txt")
        name = (
            info.find("h4").get_text(strip=True).split(" ")[0]
            if info.find("h4").get_text(strip=True)
            else "이름 정보 없음"
        )

        party_dd = info.find("p", class_="party_highlight")
        party = "정당 정보 없음"
        if party_dd:
            party = party_dd.get_text(strip=True).replace("정당 : ", "")
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_184(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """전라남도 함평군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("div", id="subContent")[0]

    total_div = mlist.find_all("div", class_="infosubcontent")
    total_div.append(mlist.find_all("div", class_="infosubcontent2"))
    for profile in total_div:
        if not profile:
            continue
        info = profile.find("div", class_="infosub_detail")
        name = (
            info.find("li", class_="infosubmem_name").get_text(strip=False)[:3]
            if info.find("li", class_="infosubmem_name").get_text(strip=True)
            else "이름 정보 없음"
        )

        party_dd = info.find("ul", class_="infosub").find_all("li")[1]
        party = "정당 정보 없음"
        if party_dd:
            party = party_dd.get_text(strip=True).replace("소속정당 : ", "")
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)
