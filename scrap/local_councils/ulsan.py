from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re

regex_pattern = re.compile(r'정\s*\S*\s*당', re.IGNORECASE)  # Case-insensitive

def scrap_70(url = 'https://council.junggu.ulsan.kr/content/member/memberName.html') -> ScrapResult:
    '''울산시 중구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all('dl'):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        
        party = "정당 정보 없음"
        party_info = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all("dd")))
        if party_info and (party_span := party_info[0].find_next('span').find_next('span')) is not None:
            party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="ulsan-junggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

def scrap_71(url = 'https://www.namgucouncil.ulsan.kr/content/member/memberName.html') -> ScrapResult:
    '''울산시 남구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all('dl'):
        name_tag = profile.find("dd", class_="name")
        name = name_tag.get_text(strip=True).replace(" 의원", "") if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_info = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all("dd")))
        if party_info and (party_span := party_info[0].find_next('span').find_next('span')) is not None:
            party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="ulsan-namgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

def scrap_72(url = 'https://www.donggu-council.ulsan.kr/source/korean/member/active.html') -> ScrapResult:
    '''울산시 동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    soup = get_soup(url, verify=False, encoding='euc-kr')
    councilors: List[Councilor] = []

    for profile in soup.find_all('div', class_='profile'):
        name_tag = profile.find("li", class_="name")
        # () 안에 있는 한자를 제거 (ex. 김영희(金英姬) -> 김영희)
        name = name_tag.get_text(strip=True).split('(')[0] if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"
        party_info = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all("li")))
        if party_info:
            party = party_info[0].get_text(strip=True).split(': ')[1]
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="ulsan-donggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

def scrap_73(url = 'https://council.bukgu.ulsan.kr/kr/member/active.do') -> ScrapResult:
    '''울산시 북구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    for profile in soup.find_all('dl', class_='profile'):
        name_tag = profile.find("strong", class_="name")
        # () 안에 있는 한자를 제거 (ex. 김영희(金英姬) -> 김영희)
        name = name_tag.get_text(strip=True).split('(')[0] if name_tag else "이름 정보 없음"
        party = "정당 정보 없음"
        party_info = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all("li")))
        if party_info:
            party = party_info[0].get_text(strip=True).split(': ')[1]
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="ulsan-bukgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

def scrap_74(url = 'https://assembly.ulju.ulsan.kr/kr/member/active') -> ScrapResult:
    '''울산시 울주군 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in soup.find_all('div', class_='profile'):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        party = '정당 정보 없음'

        # 프로필보기 링크 가져오기
        profile_link = profile.find('a', class_='start')
        if profile_link:
            profile_url = base_url + profile_link['href']
            profile_soup = get_soup(profile_url, verify=False)
            party_info = profile_soup.find('em', string=regex_pattern)
            if party_info and (party_span := party_info.find_next('span')) is not None:
                party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="ulsan_uljugun",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_70())