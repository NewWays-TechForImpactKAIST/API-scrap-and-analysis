from scrap.local_councils import *


def scrap_154(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 남원시"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("ul", class_="info"):
        name_tag = profile.find("span", class_="name")
        name = name_tag.get_text(strip=True).split()[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_155(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 김제시"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="bbs_member"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_156(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 완주군"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []
    memberlist = soup.find("div", class_="card-member")

    for profile in memberlist.find_all("li"):
        name_tag = profile.find("div", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_157(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 진안군"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_160(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 임실군"""
    # TODO: js로 동적으로 읽어옴
    raise NotImplementedError


def scrap_161(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 순창군"""
    # TODO: js로 동적으로 읽어옴
    raise NotImplementedError


def scrap_162(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 고창군"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="con_mem"):
        name_tag = profile.find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_163(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 부안군"""
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    profiles = soup.find_all("div", class_="person")
    profiles = profiles[1:]  # 첫 번째 태그는 홈페이지 목록

    for profile in profiles:
        name_tag = profile.find("p", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_tags = profile.find_all("li")
        for party_tag in party_tags:
            if "소속정당" in party_tag.text:
                party = party_tag.find_next("span").get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_164(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라남도 목포시"""
    base_url = "https://council.mokpo.go.kr/"
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name").get_text(strip=True)
        name = name_tag if name_tag else "이름 정보 없음"
        name = name.split("(")[0]  # 괄호 안에 있는 한자는 제외

        member_link = profile.find("a", class_="start")["href"]
        member_soup = get_soup(base_url + member_link)

        party_tag = member_soup.find("ul", class_="profile_list")
        party = (
            party_tag.select_one("li:contains('정 당')").text.replace("정 당:", "").strip()
        )

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_165(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라남도 여수시"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("li", class_="name").get_text(strip=True)
        name = name_tag if name_tag else "이름 정보 없음"
        name = name.split("(")[0]  # 괄호 안에 있는 한자는 제외

        party_tag = [li for li in soup.find_all("li") if "소속정당" in li.get_text()]
        party = party_tag[0].get_text() if party_tag else "정당 정보 없음"

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


def scrap_167(
    url,
    cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """전라북도 나주시"""
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("dt")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ret_local_councilors(cid, councilors)


if __name__ == "__main__":
    print(scrap_167())
