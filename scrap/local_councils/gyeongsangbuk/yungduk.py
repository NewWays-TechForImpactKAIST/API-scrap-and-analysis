from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import requests

def scrap_yungduk(url = 'https://council.yd.go.kr/kr/member/active') -> ScrapResult:
    '''영덕시 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all('div', class_='card_area')

    for profile in mlist:
        info = profile.find_all('li')
        if info:
            name = profile.find("dt").get_text(strip=True).split("(")[0] if profile.find("dt").get_text(strip=True) else "이름 정보 없음"

            party = "정당 정보 없음"
            party_dd = info[3].get_text(strip=True).replace("정당: ", "")
            if party_dd:
                party = party_dd
            councilors.append(Councilor(name=name, jdName=party))

    return ScrapResult(
        council_id="yungduk",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_yungduk())