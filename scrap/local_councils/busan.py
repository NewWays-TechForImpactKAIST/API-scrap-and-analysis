import os

from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup, get_selenium, By


def scrap_26(
    url="https://www.bsjunggu.go.kr/council/board/list.junggu?boardId=BBS_0000118&menuCd=DOM_000000503003000000&contentsSid=755&cpath=%2Fcouncil",
) -> ScrapResult:
    """부산시 중구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find("div", class_="bbs_blog council").find_all("dl"):
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

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-junggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_27(
    url="https://www.bsseogu.go.kr/council/board/list.bsseogu?boardId=BBS_0000097&categoryCode1=8&menuCd=DOM_000000603001000000&contentsSid=785&cpath=%2Fcouncil",
) -> ScrapResult:
    """부산시 서구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in soup.find_all("div", class_="intro"):
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

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-seogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_28(
    url="https://www.bsdonggu.go.kr/council/index.donggu?menuCd=DOM_000000502004000000",
) -> ScrapResult:
    """부산시 동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="council_box"):
        name_tag = profile.find_next("span", class_="n2")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find_next("span", class_="n1")
        if party_info:
            party = party_info.get_text(strip=True).split("(")[1][:-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-donggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_29(url="https://www.yeongdo.go.kr/council/01211/01212.web") -> ScrapResult:
    """부산시 영도구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="even-grid gap3pct panel1 p01205bg"):
        name_tag = profile.find_next("strong", class_="h1 title")
        name = (
            name_tag.get_text(strip=True).split(" ")[0].strip()
            if name_tag
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-yeongdogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_30(
    url="https://council.busanjin.go.kr/content/member/member.html",
) -> ScrapResult:
    """부산시 부산진구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False).find("ul", class_="mlist")
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl"):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find_all("b")[2]
        if party_info:
            party = party_info.find_next("span", class_="itemContent").get_text(
                strip=True
            )

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-busanjingu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_31(
    url="http://council.dongnae.go.kr/source/kr/member/active.html",
) -> ScrapResult:
    """부산시 동래구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for name_tag in soup.find_all("li", class_="name"):
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = name_tag.find_next("li").find_next("li")
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-dongnaegu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_32(url="https://council.bsnamgu.go.kr/kr/member/active") -> ScrapResult:
    """부산시 남구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl", class_="profile"):
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

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-namgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_33(
    url="https://www.bsbukgu.go.kr/council/index.bsbukgu?menuCd=DOM_000000808001001000",
) -> ScrapResult:
    """부산시 북구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl", class_="info"):
        name_tag = profile.find("span")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", string="소속정당")
        if party_info:
            party = party_info.parent.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-bukgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_34(
    url="https://council.haeundae.go.kr/board/list.do?boardId=BBS_0000096&categoryCode1=08&menuCd=DOM_000000702001001000&contentsSid=330",
) -> ScrapResult:
    """부산시 해운대구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False).find("div", class_="initial_list")
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for name_tag in soup.find_all("dd"):
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        # 프로필보기 링크 가져오기
        profile_link = name_tag.find("a")
        if profile_link:
            profile_url = base_url + profile_link["href"]
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find("span", string="소속정당")
            if party_info and (party_span := party_info.parent) is not None:
                party = party_span.text[4:].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-haeundaegu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_35(
    url="https://council.gijang.go.kr/source/korean/member/active.html",
) -> ScrapResult:
    """부산시 기장군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("ul", class_="wulli bul02"):
        li_tags = profile.find_all("li")

        name_tag = li_tags[0]
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = li_tags[2]
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-gijanggun",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_36(
    url="https://www.saha.go.kr/council/congressMember/list03.do?mId=0403000000",
) -> ScrapResult:
    """부산시 사하구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for district_tag in soup.find_all("div", class_="list_member"):
        for name_tag in district_tag.find_all("h4", class_="name"):
            name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

            party = "정당 정보 없음"
            party_info = name_tag.find_next("span", string="소속당  : ")
            if party_info:
                party = party_info.parent.get_text(strip=True)[7:].strip()

            councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-sahagu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_37(
    url="https://council.geumjeong.go.kr/index.geumj?menuCd=DOM_000000716001000000",
) -> ScrapResult:
    """부산시 금정구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False).find("div", class_="council_list")
    councilors: list[Councilor] = []

    for profile in soup.find_all("a"):
        name_tag = profile.find("span", class_="tit").find("span")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        profile_url = profile["href"][:65] + "1" + profile["href"][66:]
        profile_soup = get_soup(profile_url, verify=False)

        party_info = profile_soup.find("span", class_="name", string="정당")
        if party_info and (party_span := party_info.parent) is not None:
            party = party_span.text[2:].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-geumjeonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_38(
    url="https://www.bsgangseo.go.kr/council/contents.do?mId=0203000000",
) -> ScrapResult:
    """부산시 강서구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile_img in soup.find_all("button", class_="btn_close"):
        profile = profile_img.find_next("dl")

        name_tag = profile.find("dd", class_="name")
        name = (
            name_tag.get_text(strip=True).split()[0].strip() if name_tag else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        party_info = profile.find("span", class_="bold", string="정당 : ")
        if party_info:
            party = party_info.parent.get_text(strip=True)[5:].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-gangseogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_39(
    url="https://www.yeonje.go.kr/council/assemblyIntro/list.do?mId=0201000000",
) -> ScrapResult:
    """부산시 연제구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
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
        councilors.append(Councilor(name, party))

    return ScrapResult(
        council_id="busan-yeonjegu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_40(
    url="https://www.suyeong.go.kr/council/index.suyeong?menuCd=DOM_000001402001001000&link=success&cpath=%2Fcouncil",
) -> ScrapResult:
    """부산시 수영구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="mem_info"):
        name_tag = profile.find("span", class_="name").find("span")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = profile.find("span", string="소속정당 :")
        if party_info:
            party = party_info.parent.get_text(strip=True)[6:].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-suyeonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


def scrap_41(
    url="https://www.sasang.go.kr/council/index.sasang?menuCd=DOM_000000202005000000",
) -> ScrapResult:
    """부산시 사상구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for district in soup.find_all("ul", class_="council_list"):
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

            councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="busan-sasanggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )


if __name__ == "__main__":
    print(scrap_39())
