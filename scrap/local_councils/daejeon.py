from scrap.local_councils import *


def scrap_65(url, cid) -> ScrapResult:
    """대전 동구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_66(url, cid) -> ScrapResult:
    """대전 중구"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당")
        if party_info:
            party = party_info.find_next("span").get_text(strip=True)
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_67(
    url,
    cid,
) -> ScrapResult:
    """대전 서구"""
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

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_68(url, cid) -> ScrapResult:
    """대전 유성구"""
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
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_69(url, cid) -> ScrapResult:
    """대전 대덕구"""
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
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)
