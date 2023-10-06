from urllib.parse import urlparse

from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup


def scrap_42(url='https://junggucouncil.daegu.kr/source/main03/main01.html?d_th=8') -> ScrapResult:
    """대전시 중구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False, encoding='euc-kr')
    councilors: list[Councilor] = []

    for profile in soup.find_all('div', class_='profile'):
        name_tag = profile.find('li', class_='name')
        name = name_tag.get_text(strip=True).split()[1].strip() if name_tag else "이름 정보 없음"

        party = '정당 정보 없음'
        party_info = name_tag.find_next('li').find_next('li')
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-junggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_43(url='https://www.donggucl.daegu.kr/content/member/member.html') -> ScrapResult:
    """대전시 동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []
    
	# 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for name_tag in soup.find_all('dd', class_='name'):
        name = name_tag.get_text(strip=True).split('(')[0].strip() if name_tag else "이름 정보 없음"
        party = '정당 정보 없음'

        profile_link = name_tag.find_next('a', class_='abtn_profile')
        if profile_link:
            profile_url = base_url + profile_link['href']
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find('th', scope='row', string='소속정당')
            if party_info and (party_span := party_info.find_next('td')) is not None:
                party = party_span.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-donggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_44(url='https://www.dgscouncil.go.kr/kr/member/active') -> ScrapResult:
    """대전시 서구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all('dl', class_='profile'):
        name_tag = profile.find('strong', class_='name')
        name = name_tag.get_text(strip=True).split('(')[0].strip() if name_tag else "이름 정보 없음"

        party = '정당 정보 없음'
        party_info = profile.find('li').find_next('li').find_next('li')
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-seogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_45(url='https://nam.daegu.kr/council/index.do?menu_id=00000548') -> ScrapResult:
    """대전시 남구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all('div', class_='profile'):
        name_tag = profile.find('span', class_='name2')
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = '정당 정보 없음'
        party_info = profile.find('span', class_='name', string='소속정당').find_next('span', class_='name3')
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-namgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_46(url='https://bukgucouncil.daegu.kr/kr/member/name.do') -> ScrapResult:
    """대전시 북구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all('div', class_='profile'):
        name_tag = profile.find('em', class_='name')
        name = name_tag.get_text(strip=True).split()[0].strip() if name_tag else "이름 정보 없음"

        party = '정당 정보 없음'
        party_info = profile.find('em', string='소속정당 : ').find_next('span')
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-bukgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_47(url='https://suseongcouncil.suseong.kr/ss_council/content/?pos=active&me_code=2010') -> ScrapResult:
    """대전시 수성구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all('div', class_='item'):
        name_tag = profile.find('p', class_='name').find('span')
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = '정당 정보 없음'
        party_info = profile.find_all('li')[2].find('span')
        if party_info:
            party = party_info.get_text(strip=True)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-suseonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_48(url='https://www.dalseocouncil.daegu.kr/content/member/member.html') -> ScrapResult:
    """대전시 달서구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for name_tag in soup.find_all('dd', class_='name'):
        name = name_tag.get_text(strip=True).split('(')[0].strip() if name_tag else "이름 정보 없음"

        party = '정당 정보 없음'
        party_info = name_tag.find_next('span', string='소속정당').parent
        if party_info:
            party = party_info.get_text(strip=True).split()[-1].strip()

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-dalseogu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_49(url='https://council.dalseong.go.kr/content/member/member.html') -> ScrapResult:
    """대전시 달성군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for name_tag in soup.find_all('dd', class_='name'):
        name = name_tag.get_text(strip=True).split('(')[0].strip() if name_tag else "이름 정보 없음"
        party = '정당 정보 없음'

        profile_link = name_tag.find_next('a', class_='abtn1')
        if profile_link:
            profile_url = base_url + profile_link['href']
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find('span', class_='item', string='소속정당')
            if party_info and (party_span := party_info.find_next('span', class_='item_content')) is not None:
                party = party_span.get_text(strip=True)
        
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="daejeon-dalseonggun",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


if __name__ == '__main__':
    print(scrap_49())