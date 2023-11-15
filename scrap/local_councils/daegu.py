from scrap.local_councils import *


def scrap_42(url, cid, args: ArgsType = None) -> ScrapResult:
    """대구 중구"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("li", class_="name")
        name = (
            name_tag.get_text(strip=True).split()[1].strip() if name_tag else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = name_tag.find_next("li").find_next("li")
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_43(url, cid, args: ArgsType = None) -> ScrapResult:
    """대구 동구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for name_tag in soup.find_all("dd", class_="name"):
        name = (
            name_tag.get_text(strip=True).split("(")[0].strip()
            if name_tag
            else "이름 정보 없음"
        )
        party = "정당 정보 없음"

        profile_link = name_tag.find_next("a", class_="abtn_profile")
        if profile_link:
            profile_url = base_url + profile_link["href"]
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find("th", scope="row", string="소속정당")
            if party_info and (party_span := party_info.find_next("td")) is not None:
                party = party_span.get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_44(url, cid, args: ArgsType = None) -> ScrapResult:
    """대구 서구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl", class_="profile"):
        name_tag = profile.find("strong", class_="name")
        name = (
            name_tag.get_text(strip=True).split("(")[0].strip()
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("li").find_next("li").find_next("li")
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_45(url, cid, args: ArgsType = None) -> ScrapResult:
    """대구 남구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("span", class_="name2")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", class_="name", string="소속정당").find_next(
            "span", class_="name3"
        )
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_46(url, cid, args: ArgsType = None) -> ScrapResult:
    """대구 북구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = (
            name_tag.get_text(strip=True).split()[0].replace("의원", "").strip()
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("em", string="소속정당 : ").find_next("span")
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_47(url, cid, args: ArgsType = None) -> ScrapResult:
    """대구 수성구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="item"):
        name_tag = profile.find("p", class_="name").find("span")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find_all("li")[2].find("span")
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_48(url, cid, args: ArgsType = None) -> ScrapResult:
    """대구 달서구"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for name_tag in soup.find_all("dd", class_="name"):
        name = (
            name_tag.get_text(strip=True).split("(")[0].strip()
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = name_tag.find_next("span", string="소속정당").parent
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def scrap_49(url, cid, args: ArgsType = None) -> ScrapResult:
    """대구 달성군"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for name_tag in soup.find_all("dd", class_="name"):
        name = (
            name_tag.get_text(strip=True).split("(")[0].strip()
            if name_tag
            else "이름 정보 없음"
        )
        party = "정당 정보 없음"

        profile_link = name_tag.find_next("a", class_="abtn1")
        if profile_link:
            profile_url = base_url + profile_link["href"]
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find("span", class_="item", string="소속정당")
            if (
                party_info
                and (party_span := party_info.find_next("span", class_="item_content"))
                is not None
            ):
                party = party_span.get_text(strip=True)

        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)
