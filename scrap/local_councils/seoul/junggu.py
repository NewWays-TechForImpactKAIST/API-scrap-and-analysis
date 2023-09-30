from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup

def scrap_junggu(url = 'https://02jgnew.council.or.kr/kr/member/active') -> ScrapResult:
    '''서울시 중구의회 페이지에서 의원 상세약력 스크랩

    :param url: 중구의회 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    parliment_soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in parliment_soup.find_all('div', class_='profile'):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        party = '정당 정보 없음'

        # 프로필보기 링크 가져오기
        profile_link = profile.find('a', class_='start')
        if profile_link:
            profile_url = base_url + profile_link['href']
            profile_soup = get_soup(profile_url, verify=False)

            party_info = profile_soup.find('em', string='소속정당 : ')
            if party_info and (party_span := party_info.find_next('span')) is not None:
                party = party_span.text

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-junggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_junggu())