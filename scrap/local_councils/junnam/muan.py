from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re

def scrap_muan(url = 'http://www.muan.or.kr/main/incumbentCouncillor.do?PID=0201') -> ScrapResult:
    '''무안 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all('ul', class_='formerCouncillor')[0]

    for profile in mlist.find_all('li', recursive=False):
        info = profile.find('div', class_='profileInfo')
        name = info.find("div", class_="infosubmem_name").get_text(strip=True) if info.find("div", class_="infosubmem_name").get_text(strip=True) else "이름 정보 없음"

        party_dd = info.find("div", class_="infoContents")
        party = "정당 정보 없음"
        if party_dd:
            party = party_dd.get_text(strip=True)
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="muan",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_muan())