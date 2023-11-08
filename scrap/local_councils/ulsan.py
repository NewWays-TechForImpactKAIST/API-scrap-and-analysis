from scrap.local_councils import *
from scrap.local_councils.basic import regex_pattern

def scrap_70(
    url, cid
) -> ScrapResult:
    """울산 중구"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("dl"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = list(
            filter(lambda x: regex_pattern.search(str(x)), profile.find_all("dd"))
        )
        if (
            party_info
            and (party_span := party_info[0].find_next("span").find_next("span"))
            is not None
        ):
            party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_71(
    url, cid
) -> ScrapResult:
    """울산 남구"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("dl"):
        name_tag = profile.find("dd", class_="name")
        name = (
            name_tag.get_text(strip=True).replace(" 의원", "") if name_tag else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = list(
            filter(lambda x: regex_pattern.search(str(x)), profile.find_all("dd"))
        )
        if (
            party_info
            and (party_span := party_info[0].find_next("span").find_next("span"))
            is not None
        ):
            party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_72(
    url, cid
) -> ScrapResult:
    """울산 동구"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: List[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("li", class_="name")
        # () 안에 있는 한자를 제거 (ex. 김영희(金英姬) -> 김영희)
        name = name_tag.get_text(strip=True).split("(")[0] if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"
        party_info = list(
            filter(lambda x: regex_pattern.search(str(x)), profile.find_all("li"))
        )
        if party_info:
            party = party_info[0].get_text(strip=True).split(": ")[1]
        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_73(url, cid) -> ScrapResult:
    """울산 북구"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all("dl", class_="profile"):
        name_tag = profile.find("strong", class_="name")
        # () 안에 있는 한자를 제거 (ex. 김영희(金英姬) -> 김영희)
        name = name_tag.get_text(strip=True).split("(")[0] if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"
        party_info = list(
            filter(lambda x: regex_pattern.search(str(x)), profile.find_all("li"))
        )
        if party_info:
            party = party_info[0].get_text(strip=True).split(": ")[1]
        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_74(url, cid) -> ScrapResult:
    """울산 울주군"""
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_link = profile.find("a", class_="start")
        if profile_link:
            profile_url = base_url + profile_link["href"]
            profile_soup = get_soup(profile_url, verify=False)
            party_info = profile_soup.find("em", string=regex_pattern)
            if party_info and (party_span := party_info.find_next("span")) is not None:
                party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


if __name__ == "__main__":
    print(scrap_70())
