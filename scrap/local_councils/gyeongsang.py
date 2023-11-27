import requests
from scrap.local_councils import *
from scrap.utils.requests import get_selenium, By
from scrap.local_councils.basic import (
    getprofiles,
    getname,
    extract_party,
    find,
    findall,
    regex_pattern,
)

party_keywords = getPartyList()
party_keywords.append("무소속")

def scrap_186(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 포항시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="mlist")[0]

    for profile in mlist.find_all("li"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True).split(" ")[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", string="정")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_188(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 경주시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        data_uid = profile.find("a", class_="btn_profile")["data-uid"]

        if data_uid:
            url = f"https://council.gyeongju.go.kr/common/async/member/{data_uid}.do"
            result = requests.get(url).json()
            name = result["name"] if result["name"] else "이름 정보 없음"
            party = result["party_nm"] if result["party_nm"] else "정당 정보 없음"

            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_189(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 김천시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="memberList")[0]

    for profile in mlist.find_all("li", recursive=False):
        name_tag = profile.find("h4")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", string=re.compile(r"소속정당\s*:", re.IGNORECASE))
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_190(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 안동시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_191(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 구미시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="mlist")[0]

    for profile in mlist.find_all("li"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", string="정")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)

def scrap_192(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 구미시"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("li", class_="name")
        name = name_tag.get_text(strip=True).split("(")[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        profile_link = profile.find_all("a")[1]
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        profile_url = base_url + profile_link["href"]
        profile = get_soup(profile_url, verify=False, encoding="euc-kr")
        party=""
        for keyword in party_keywords:
            if keyword in profile.text:
                party=keyword
                break
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_194(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 상주시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name").find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_195(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 문경시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        data_uid = profile.find("a", class_="btn_profile")["data-uid"]

        if data_uid:
            url = f"https://council.gbmg.go.kr/common/async/member/{data_uid}.do"
            result = requests.get(url).json()
            name = result["name"] if result["name"] else "이름 정보 없음"
            party = result["party_nm"] if result["party_nm"] else "정당 정보 없음"

            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_196(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 예천군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        data_uid = profile.find("a", class_="btn_profile")["data-uid"]

        if data_uid:
            url = f"https://www.ycgcl.kr/common/async/member/{data_uid}.do"
            result = requests.get(url).json()
            name = result["name"] if result["name"] else "이름 정보 없음"
            party = result["party_nm"] if result["party_nm"] else "정당 정보 없음"

            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_197(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 경산시"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: List[Councilor] = []
    for profile in soup.find_all('div', class_='memberL') + soup.find_all('div', class_='memberR'):
        party = profile.find_previous('h4', class_='title').text.strip()
        assert(party in party_keywords)
        name = profile.find('dt').text.strip()
        
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_198(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 청도군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_199(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 고령군"""
    browser = get_selenium(url)
    councilors: list[Councilor] = []
    for profile in browser.find_elements(By.CSS_SELECTOR, "div[class='profile']"):
        name_tag = profile.find_element(By.CSS_SELECTOR, "em[class='name']")
        name = name_tag.text.strip().split("\r")[0] if name_tag else "이름 정보 없음"
        party = ""
        for keyword in party_keywords:
            if keyword in profile.text:
                party = keyword
                break
        party = "정당 정보 없음"
        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_201(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 칠곡군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="memberUl")[0]

    for profile in mlist.find_all("li", recursive=False):
        info = profile.find_all("dd")
        if info:
            name = (
                profile.find("dd", class_="name").get_text(strip=True)
                if profile.find("dd", class_="name").get_text(strip=True)
                else "이름 정보 없음"
            )

            party = "정당 정보 없음"
            party_dd = info[3].get_text(strip=True).replace("정당 : ", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_202(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 군위군"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("li", class_="name")
        name = name_tag.get_text(strip=True).split("(")[0] if name_tag else "이름 정보 없음"
        link = profile.find("p", class_="btn").find("a")["href"]
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        profile_url = base_url + link
        profile = get_soup(profile_url, verify=False, encoding="euc-kr")
        party=""
        for keyword in party_keywords:
            if keyword in profile.text:
                party=keyword
                break
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)

def scrap_203(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 의성군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        data_uid = profile.find("a", class_="btn_profile")["data-uid"]

        if data_uid:
            url = f"http://www.cus.go.kr/common/async/member/{data_uid}.do"
            result = requests.get(url).json()
            name = result["name"] if result["name"] else "이름 정보 없음"
            party = result["party_nm"] if result["party_nm"] else "정당 정보 없음"

            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)

def scrap_204(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 청송군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="box3vm1"):
        name_tag = profile.find("span", class_="t3")
        name = name_tag.get_text(strip=True).split()[-1] if name_tag else "이름 정보 없음"
        link = profile.find("a", class_="button")["href"]
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        profile_url = base_url + link
        profile = get_soup(profile_url, verify=False)
        link = profile.find('a', text='의원소개', href=True)
        profile_url = base_url + link['href']
        profile = get_soup(profile_url, verify=False)

        party=""
        for keyword in party_keywords:
            if keyword in profile.text:
                party=keyword
                break
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)

def scrap_206(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 영덕군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("div", class_="card_area")

    for profile in mlist:
        info = profile.find_all("li")
        if info:
            name = (
                profile.find("dt").get_text(strip=True).split("(")[0]
                if profile.find("dt").get_text(strip=True)
                else "이름 정보 없음"
            )

            party = "정당 정보 없음"
            party_dd = info[3].get_text(strip=True).replace("정당: ", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_208(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상북도 울진군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        data_uid = profile.find("a", class_="btn_profile")["data-uid"]

        if data_uid:
            url = f"http://council.uljin.go.kr/common/async/member/{data_uid}.do"
            result = requests.get(url).json()
            name = result["name"] if result["name"] else "이름 정보 없음"
            party = result["party_nm"] if result["party_nm"] else "정당 정보 없음"

            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_209(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 창원시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("ul", class_="mlist")[0]

    for profile in mlist.find_all("li"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", string="정")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_210(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 진주시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name").find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_212(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 고성군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_213(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 사천시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_214(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 김해시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("div", class_="card_area")

    for profile in mlist:
        info = profile.find_all("li")
        if info:
            name = (
                profile.find("dt").get_text(strip=True).split("(")[0]
                if profile.find("dt").get_text(strip=True)
                else "이름 정보 없음"
            )

            party = "정당 정보 없음"
            party_dd = info[2].get_text(strip=True).replace("정 당 :", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_215(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 밀양시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="council_box"):
        name_tag = (
            profile.find("span", string="이름").find_next("span").get_text(strip=True)
        )
        name = name_tag if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = (
            profile.find("span", string="소속정당").find_next("span").get_text(strip=True)
        )
        if party_info:
            party = party_info
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_216(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 거제시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("dl")

    for profile in mlist:
        info = profile.find_all("li")
        if info:
            name = (
                profile.find("dt").get_text(strip=True)
                if profile.find("dt").get_text(strip=True)
                else "이름 정보 없음"
            )

            party = "정당 정보 없음"
            party_dd = info[2].get_text(strip=True).replace("정당 :", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_217(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 의령군"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_218(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 함안군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("div", class_="column")

    for profile in mlist:
        name = (
            profile.find("h2").get_text(strip=True).split("\n")[0]
            if profile.find("h2").get_text(strip=True)
            else "이름 정보 없음"
        )
        info = profile.find_all("li")
        if info:
            party = "정당 정보 없음"
            party_dd = info[2].get_text(strip=True).replace("정당", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_219(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 창녕군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("div", class_="card_area")

    for profile in mlist:
        info = profile.find_all("li")
        if info:
            name = (
                profile.find("dt").get_text(strip=True).split("(")[0]
                if profile.find("dt").get_text(strip=True)
                else "이름 정보 없음"
            )

            party = "정당 정보 없음"
            party_dd = info[2].get_text(strip=True).replace("정 당 :", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_220(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 양산시"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="member"):
        name_tag = profile.find("strong", class_="name")
        name = name_tag.get_text(strip=True).split("(")[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("strong", string="정   당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_222(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 남해군"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("li", class_="name")
        name = name_tag.get_text(strip=True).split("(")[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find_all("li")[3]
        if party_info:
            party = party_info.get_text(strip=True).replace("소속정당 : ", "")
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_223(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 함양군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_224(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 산청군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find("ul", class_="comment_list")
    lis = mlist.find_all("li", recursive=False)
    for profile in lis:
        print(profile)
        info = profile.find_all("li")
        name = (
            profile.find("span", class_="name").get_text(strip=True)
            if profile.find("span", class_="name").get_text(strip=True)
            else "이름 정보 없음"
        )
        party = "정당 정보 없음"

        party_dd = info[3].get_text(strip=True).replace("소속정당", "")
        if party_dd:
            party = party_dd
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_226(
    url,
    cid,
    args: ArgsType = None,
) -> ScrapResult:
    """경상남도 합천군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all("dl", class_="member")

    for profile in mlist:
        info = profile.find_all("li")
        if info:
            name = (
                info[0].get_text(strip=True).split("(")[0]
                if info[0].get_text(strip=True)
                else "이름 정보 없음"
            )

            party = "정당 정보 없음"
            party_dd = info[3].get_text(strip=True).replace("소속정당 : ", "")
            if party_dd:
                party = party_dd.replace(" ", "")
            councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)
