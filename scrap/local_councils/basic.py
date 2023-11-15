from scrap.utils.requests import get_selenium, By
from selenium.common.exceptions import NoSuchElementException
from scrap.local_councils import *
import re
import requests
import copy
import traceback

regex_pattern = re.compile(r"정\s*\S*\s*당", re.IGNORECASE)  # Case-insensitive
party_keywords = getPartyList()
party_keywords.append("무소속")


def find(soup, element, class_=None):
    if class_ is None:
        return soup.find(element)
    else:
        return soup.find(element, class_)


def findall(soup, element, class_=None):
    if class_ is None:
        return soup.find_all(element)
    else:
        return soup.find_all(element, class_)


def sel_find(driver, element, class_=None):
    if class_ is None:
        return driver.find_element(By.TAG_NAME, element)
    else:
        return driver.find_element(By.CSS_SELECTOR, f"{element}.{class_}")


def sel_findall(driver, element, class_=None):
    if class_ is None:
        return driver.find_elements(By.TAG_NAME, element)
    else:
        return driver.find_elements(By.CSS_SELECTOR, f"{element}.{class_}")


def getprofiles(soup, element, class_, memberlistelement, memberlistclass_):
    # 의원 목록 사이트에서 의원 프로필을 가져옴
    if memberlistelement is not None:
        try:
            soup = findall(soup, memberlistelement, class_=memberlistclass_)[0]
        except Exception:
            raise RuntimeError("[basic.py] 의원 목록 사이트에서 의원 프로필을 가져오는데 실패했습니다.")
    return findall(soup, element, class_)


def sel_getprofiles(driver, element, class_, memberlistelement, memberlistclass_):
    # 의원 목록 사이트에서 의원 프로필을 가져옴
    if memberlistelement is not None:
        try:
            member_list = sel_findall(driver, memberlistelement, memberlistclass_)[0]
        except Exception:
            raise RuntimeError("[basic.py] 의원 목록 사이트에서 의원 프로필을 가져오는데 실패했습니다.")
    else:
        member_list = driver

    return sel_findall(member_list, element, class_)


def getDataFromAPI(url_format, data_uid, name_id, party_id) -> Councilor:
    # API로부터 의원 정보를 가져옴
    url = url_format.format(data_uid)
    result = requests.get(url).json()
    return Councilor(
        name=result[name_id] if result[name_id] else "이름 정보 없음",
        jdName=result[party_id] if result[party_id] else "정당 정보 없음",
    )


def getname(profile, element, class_, wrapper_element, wrapper_class_):
    # 의원 프로필에서 의원 이름을 가져옴
    if wrapper_element is not None:
        profile = findall(profile, wrapper_element, class_=wrapper_class_)[0]
    name_tag = find(profile, element, class_)
    if name_tag.find("span"):
        name_tag = copy.copy(name_tag)
    # 1. span 태그 안의 것들을 다 지움
    for span in name_tag.find_all("span"):
        span.decompose()
    # 2. a 태그 안의 것들을 다 지움 : 예. 인천 서구, 안에 '개인홈페이지' 링크가 들음.
    for a_tag in name_tag.find_all("a"):
        a_tag.extract()
    name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
    # 3. strong 태그 안에 이름이 있는 경우 : name이 긴지 체크한 뒤 strong 태그 안을 받아옴.
    # 은평구, 수원시 등.
    if name_tag.strong is not None:
        name = name_tag.strong.get_text(strip=True) if name_tag.strong else "이름 정보 없음"
    name = name.split("(")[0].split(":")[-1].strip()  # 이름 뒷 한자이름, 앞 '이   름:' 제거
    # TODO : 만약 이름이 우연히 아래 단어를 포함하는 경우를 생각해볼만 함.
    if len(name) > 3:
        # 수식어가 이름 앞이나 뒤에 붙어있는 경우
        for keyword in ["부의장", "의원", "의장"]:  # 119, 강서구 등
            if keyword in name:
                name = name.replace(keyword, "").strip()
        for keyword in party_keywords:
            if keyword in name:  # 인천 서구 등
                name = name.replace(keyword, "").strip()
                break
    maybe_name = name.split()[0]  # 이름 뒤에 직책이 따라오는 경우
    if len(maybe_name) == 1:  # 외자 이름이 띄어쓰기 때문에 분리된 경우
        name = "".join(name.split()[0:2])
    else:
        name = maybe_name
    return name


def sel_getname(profile, element, class_, wrapper_element, wrapper_class_):
    # 의원 프로필에서 의원 이름을 가져옴
    if wrapper_element is not None:
        profile = sel_find(profile, wrapper_element, class_=wrapper_class_)
    name_tag = sel_find(profile, element, class_)
    # print(name_tag.text)
    name = name_tag.text.strip() if name_tag else "이름 정보 없음"
    # strong 태그 안에 이름이 있는 경우 : name이 긴지 체크한 뒤 strong 태그 안을 받아옴.
    # 은평구, 수원시 등.
    try:
        strong_element = sel_find(name_tag, "strong")
        if strong_element is not None:
            name = strong_element.text.strip()
    except NoSuchElementException:
        pass
    # print(name+"\n")
    if name == "":
        return "231114"
    name = name.split("(")[0].split(":")[-1].strip()  # 이름 뒷 한자이름, 앞 '이   름:' 제거
    # TODO : 만약 이름이 우연히 아래 단어를 포함하는 경우를 생각해볼만 함.
    if len(name) > 3:
        # 수식어가 이름 앞이나 뒤에 붙어있는 경우
        for keyword in ["부의장", "의원", "의장"]:  # 119, 강서구 등
            if keyword in name:
                name = name.replace(keyword, "").strip()
        for keyword in party_keywords:
            if keyword in name:  # 인천 서구 등
                name = name.replace(keyword, "").strip()
                break
    print(name, "is name\n")
    maybe_name = name.split()[0]  # 이름 뒤에 직책이 따라오는 경우
    if len(maybe_name) == 1:  # 외자 이름이 띄어쓰기 때문에 분리된 경우
        name = "".join(name.split()[0:2])
    else:
        name = maybe_name
    return name


def extract_party(string):
    for keyword in party_keywords:
        if keyword in string:
            return keyword
    return None


def goto_profilesite(profile, wrapper_element, wrapper_class_, wrapper_txt, url):
    # 의원 프로필에서 프로필보기 링크를 가져옴
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    # 프로필보기 링크 가져오기
    profile_link = find(profile, wrapper_element, class_=wrapper_class_)
    if wrapper_txt is not None:
        profile_links = findall(profile, "a", class_=wrapper_class_)
        profile_link = [link for link in profile_links if link.text == wrapper_txt][0]
    if profile_link is None:
        raise RuntimeError("[basic.py] 의원 프로필에서 프로필보기 링크를 가져오는데 실패했습니다.")
    # if base_url[-1] != '/':
    #     base_url = base_url + '/'
    profile_url = base_url + profile_link["href"]
    try:
        profile = get_soup(profile_url, verify=False)
    except Exception:
        raise RuntimeError("[basic.py] '//'가 있진 않나요?", " url: ", profile_url)
    return profile


def sel_goto_profilesite(
    profile, wrapper_element, wrapper_class_=None, wrapper_txt=None, url=None
):
    # 의원 프로필에서 프로필보기 링크를 가져옴
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    # 프로필보기 링크 가져오기
    if wrapper_txt is None:
        profile_link = sel_find(profile, wrapper_element, class_=wrapper_class_)
    else:
        profile_links = sel_findall(profile, wrapper_element, class_=wrapper_class_)
        profile_link = [link for link in profile_links if link.text == wrapper_txt][0]
    if profile_link is None:
        raise RuntimeError("[basic.py] 의원 프로필에서 프로필보기 링크를 가져오는데 실패했습니다.")
    # print(profile_link.get_attribute("href"))

    # print("clicked")
    # # 프로필 사이트 로딩을 기다림
    # try:
    #     WebDriverWait(profile, 10).until(EC.url_contains(profile_link.get_attribute("href")))  # 10초 동안 기다림
    # except Exception:
    #     raise RuntimeError("[basic.py] 프로필 사이트로 이동하는데 실패했습니다.")
    return get_selenium(profile_link.get_attribute("href"))


def getpty(profile, element, class_, wrapper_element, wrapper_class_, wrapper_txt, url):
    # 의원 프로필에서 의원이 몸담는 정당 이름을 가져옴
    if wrapper_element is not None:
        profile = goto_profilesite(
            profile, wrapper_element, wrapper_class_, wrapper_txt, url
        )
    party_pulp_list = list(
        filter(
            lambda x: regex_pattern.search(str(x)), findall(profile, element, class_)
        )
    )
    if party_pulp_list == []:
        raise RuntimeError("[basic.py] 정당정보 regex 실패")
    party_pulp = party_pulp_list[0]
    party_string = party_pulp.get_text(strip=True).split(" ")[-1]
    while True:
        if (party := extract_party(party_string)) is not None:
            return party
        if (party_pulp := party_pulp.find_next("span")) is not None:
            party_string = party_pulp.text.strip().split(" ")[-1]
        else:
            return "[basic.py] 정당 정보 파싱 불가"


def getpty_easy(profile, wrapper_element, wrapper_class_, wrapper_txt, url):
    # 의원 프로필에서 의원이 몸담는 정당 이름을 가져옴
    if wrapper_element is not None:
        profile = goto_profilesite(
            profile, wrapper_element, wrapper_class_, wrapper_txt, url
        )
    party = extract_party(profile.text)
    assert party is not None
    return party


def sel_getpty_easy(
    profile, wrapper_element, wrapper_class_=None, wrapper_txt=None, url=None
):
    # 의원 프로필에서 의원이 몸담는 정당 이름을 가져옴
    if wrapper_element is not None:
        page_content = sel_goto_profilesite(
            profile, wrapper_element, wrapper_class_, wrapper_txt, url
        ).page_source
        for keyword in party_keywords:
            if keyword in page_content:
                return keyword
        raise RuntimeError("[basic.py/get_selenium_party_easy] Party not found")
    else:
        party = extract_party(profile.text)
        assert party is not None
        return party


def scrap_basic(url, cid, args: ScrapBasicArgument, encoding="utf-8") -> ScrapResult:
    """의원 상세약력 스크랩
    :param url: 의원 목록 사이트 url
    :param cid: 의회 id
    :param encoding: 받아온 soup 인코딩
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding=encoding)
    councilors: list[Councilor] = []

    profiles = getprofiles(
        soup, args.pf_elt, args.pf_cls, args.pf_memlistelt, args.pf_memlistcls
    )
    print(cid, "번째 의회에는,", len(profiles), "명의 의원이 있습니다.")  # 디버깅용.

    for profile in profiles:
        name = party = ""
        try:
            name = getname(
                profile,
                args.name_elt,
                args.name_cls,
                args.name_wrapelt,
                args.name_wrapcls,
            )
        except Exception as e:
            raise RuntimeError("[basic.py] 의원 이름을 가져오는데 실패했습니다. 이유 : " + str(e))
        try:
            party = getpty(
                profile,
                args.pty_elt,
                args.pty_cls,
                args.pty_wrapelt,
                args.pty_wrapcls,
                args.pty_wraptxt,
                url,
            )
        except Exception as e:
            try:
                party = getpty_easy(
                    profile, args.pty_wrapelt, args.pty_wrapcls, args.pty_wraptxt, url
                )
            except Exception:
                raise RuntimeError("[basic.py] 의원 정당을 가져오는데 실패했습니다. 이유: " + str(e))
        councilors.append(Councilor(name=name, jdName=party))

    return ret_local_councilors(cid, councilors)


def sel_scrap_basic(url, cid, args: ScrapBasicArgument) -> ScrapResult:
    """의원 상세약력 스크랩
    :param url: 의원 목록 사이트 url
    :param cid: 의회 id
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    browser = get_selenium(url)
    councilors: list[Councilor] = []

    profiles = sel_getprofiles(
        browser, args.pf_elt, args.pf_cls, args.pf_memlistelt, args.pf_memlistcls
    )
    print(cid, "번째 의회에는,", len(profiles), "명의 의원이 있습니다.")  # 디버깅용.

    for profile in profiles:
        name = party = ""
        try:
            name = sel_getname(
                profile,
                args.name_elt,
                args.name_cls,
                args.name_wrapelt,
                args.name_wrapcls,
            )
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(
                "[basic.py/selenium] 의원 이름을 가져오는데 실패했습니다. 이유 : " + str(e)
            )
        if name == "231114":
            continue
        try:
            party = sel_getpty_easy(
                profile, args.pty_wrapelt, args.pty_wrapcls, args.pty_wraptxt, url
            )
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError("[basic.py/selenium] 의원 정당을 가져오는데 실패했습니다. 이유: " + str(e))

        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


if __name__ == "__main__":
    args3 = ScrapBasicArgument(
        pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
    )
    print(scrap_basic("https://www.yscl.go.kr/kr/member/name.do", 3, args3))  # 서울 용산구
