from scrap.local_councils import *
from scrap.local_councils.basic import *

def scrap_124(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """충청북도 청주시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    memcontent = soup.find("div", class_="memContent")

    for profile in memcontent.find_all("li"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        for tag in profile.find_all("dd"):
            tag_text = tag.get_text(strip=True)
            if "소속정당" in tag_text:
                party = tag_text.split(":")[1].strip()
                break

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_125(
url, cid,    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """충청북도 충주시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    memcontent = soup.find("ul", class_="mlist")

    for profile in memcontent.find_all("li"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        for tag in profile.find_all("dd"):
            if tag.span and "소속정당" in tag.span.get_text(strip=True):
                party = tag.get_text(strip=True).split(":")[1].strip()
                break

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_126(
url, cid,    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """충청북도 제천시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    party_list = soup.find("div", class_="tab_obj n2")
    party_tags = party_list.find_all("h4")

    for party_tag in party_tags:
        party = party_tag.get_text(strip=True)

        profile_wrapper = party_tag.find_next("div", class_="intro_council_list")

        for profile in profile_wrapper.find_all("div", class_="intro_council_box"):
            name_tag = profile.find("p", class_="name")
            name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
            councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_132(
url, cid,    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """충청북도 제천시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    party_list = soup.find("div", {"id": "tabs-2"})
    party_tags = party_list.find_all("h3")

    for party_tag in party_tags:
        party = party_tag.get_text(strip=True)

        profile_wrapper = party_tag.find_next("div", class_="member_profile")

        for profile in profile_wrapper.find_all("li"):
            name_tag = profile.find("h4", class_="h0")
            if name_tag:
                name = name_tag.get_text(strip=True).split()[0]  # 김철수 의원 -> 김철수
                councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_134(
url, cid,    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """충청북도 증평군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: List[Councilor] = []

    profiles = soup.find_all("div", class_="active_list")

    for profile in profiles:
        name_tag = profile.find("span", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        ul_tags = profile.find("ul", class_="profile").find_all("li")
        for tag in ul_tags:
            if "소속정당" in tag.get_text():
                party = tag.get_text().replace("소속정당 : ", "").strip()
                break

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_140(
url, cid,    args: ScrapBasicArgument = None
) -> ScrapResult:
    """충청남도 태안군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    member_list = soup.find("div", class_="member_list")

    for profile in member_list.find_all("dl"):
        name_tag = profile.find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party_tag = profile.find("li", class_="jungdang")
        party = party_tag.get_text(strip=True) if party_tag else "정당 정보 없음"

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_142(
url, cid,    args
) -> ScrapResult:
    """충청남도 논산시"""
    base_url = "https://www.nonsancl.go.kr/kr/member/profile_popup?uid="
    soup = get_soup(url)
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl", class_="profile"):
        name_tag = profile.find("em", class_="name").get_text(strip=True)
        name = name_tag if name_tag else "이름 정보 없음"

        data_uid = profile.find("a", class_="start")["data-uid"]
        member_soup = get_soup(base_url + data_uid)

        party_tag = member_soup.find("ul", class_="profile_list")
        party = (
            party_tag.select_one("li:contains('소속정당')")
            .text.replace("소속정당:", "")
            .strip()
        )

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


if __name__ == "__main__":
    print(scrap_142())
