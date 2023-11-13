from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re

def scrap_hamppyeong(url = 'https://www.hpcouncil.go.kr/main/incumbentCouncillor.do?PID=0201&item=01') -> ScrapResult:
    '''무안 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    
    soup = get_soup(url, verify=False)
    councilors: List[Councilor] = []
    mlist = soup.find_all('div', id='subContent')[0]

    total_div = mlist.find_all("div", class_="infosubcontent")
    total_div.append(mlist.find_all("div", class_="infosubcontent2"))
    for profile in total_div:
        if not profile:
            continue
        info = profile.find('div', class_='infosub_detail')
        name = info.find("li", class_="infosubmem_name" ).get_text(strip=False)[:3] if info.find("li", class_="infosubmem_name" ).get_text(strip=True) else "이름 정보 없음"

        party_dd = info.find("ul", class_="infosub").find_all('li')[1]
        party = "정당 정보 없음"
        if party_dd:
            party = party_dd.get_text(strip=True).replace("소속정당 : ", "")
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="yeonggwang",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_hamppyeong())