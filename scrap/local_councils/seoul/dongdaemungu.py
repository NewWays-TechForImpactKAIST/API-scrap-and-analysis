from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup

def scrap_dongdaemungu(url = 'http://council.ddm.go.kr/citizen/menu1.asp') -> ScrapResult:
    '''서울시 동대문구 페이지에서 의원 상세약력 스크랩

    :param url: 동대문구의회 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    parliment_soup = get_soup(url, verify=False, encoding='euc-kr')
    councilors: List[Councilor] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in parliment_soup.find_all('div', class_='intro_text tm_lg_6'):
        name = profile.find('p', class_='intro_text_title').string.strip().split(' ')[0]
        party = '정당 정보 없음'

        # 프로필보기 링크 가져오기
        profile_link = profile.find('a')
        if profile_link:
            profile_url = base_url + '/assemblyman/greeting/menu02.asp?assembly_id=' + profile_link['href'][1:]
            profile_soup = get_soup(profile_url, verify=False, encoding='euc-kr')

            profile_info = profile_soup.find('div', class_='profileTxt')
            if profile_info:
                profile_string = profile_info.get_text().strip().split('\xa0')
                idx = profile_string.index('소속정당')
                party = profile_string[idx + 2]

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="seoul-dongdaemungu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_dongdaemungu())