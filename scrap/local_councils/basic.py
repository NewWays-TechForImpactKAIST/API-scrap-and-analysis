from urllib.parse import urlparse

from typing import List
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re

regex_pattern = re.compile(r'정\s*\S*\s*당', re.IGNORECASE)  # Case-insensitive
party_keywords = ['국민의힘', '더불어민주당', '정의당', '진보당', '기본소득당', '시대전환', '한국의희망', '무소속'] # 이상 원내정당.
# 원외정당의 경우, 나무위키 피셜이지만 현재는 지방의회 진출당이 없다. 사실 당 이름이 매번 바뀌므로 다른 어프로치를 찾아야 할 듯.. 

def scrap_basic(url = 'https://www.yscl.go.kr/kr/member/name.do', council_id = "seoul-yongsangu", encoding = None) -> ScrapResult:
    '''의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    soup = get_soup(url, verify=False)
    if encoding:
        soup = get_soup(url, verify=False, encoding=encoding)
    party_in_soup = any(keyword in soup.text for keyword in party_keywords)
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    councilors: List[Councilor] = []
    profiles = soup.find_all("div", class_="profile")
    if profiles == []:
        profiles = soup.find_all("div", class_="card_area")
    if profiles == []:
        profiles = soup.find_all("dl")
    if profiles == []: # 강서구
        profiles = soup.find_all("div", class_='memberbox')
    if profiles == []: # 마포구
        memberlist = soup.find_all("ul", class_='memberList')
        profiles = memberlist[0].find_all('div', class_='wrap')
    print(council_id, '에는,', len(profiles), '명의 의원이 있습니다.') # 디버깅용. 
    for profile in profiles:
        name_tag = profile.find(class_="name")
        if name_tag is None:
            name_tag = profile.find("dt")
        if name_tag is None and (wrapper := profile.find_all("div", class_='right')) != []: # 마포구
            name_tag = wrapper[0].find('h4')
        if name_tag is None and (wrapper := profile.find_all("li", class_='first-child')) != []: # 강서구
            name_tag = wrapper[0].find('span')
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        if len(name) > 10: # strong태그 등 많은 걸 name 태그 안에 포함하는 경우. 은평구 등.
            name = name_tag.strong.get_text(strip=True) if name_tag else "이름 정보 없음"
        name = name.split('(')[0] # 뒷 한자이름 제거 
        if name[-2:] == '의원': # 의원이라는 글자가 이름 앞에 붙어있는 경우. 강서구 등.
            name = name[:-2].strip()
        
        party = "정당 정보 없음"
        if party_in_soup:
            party_info = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all("li")))
            if party_info is None:
                party_info = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all("dd")))
            if party_info is None:
                party_info = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all("em")))
            if party_info is None:
                pass
            else:
                party = party_info[0].get_text(strip=True).split(' ')[-1].strip()
                if party in party_keywords:
                    pass
                else:
                    party = "정당 정보 없음"
                    if (party_span := party_info[0].find_next('span')) is not None:
                        party = party_span.text.split(' ')[-1]
                        while not any(keyword in party for keyword in party_keywords):
                            party_span = party_span.find_next('span')
                            party = party_span.text.split(' ')[-1]
                        party = party.strip()
                    else:
                        pass
        else:
            # 프로필보기 링크 가져오기
            profile_link = profile.find('a', class_='start')
            if profile_link:
                profile_url = base_url + profile_link['href']
                profile_soup = get_soup(profile_url, verify=False)
                party_info = profile_soup.find('em', string=regex_pattern)
                if party_info and (party_span := party_info.find_next('span')) is not None:
                    party = party_span.text.split(' ')[-1]

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id,
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    # print(scrap_basic('https://council.jongno.go.kr/council/councilAsemby/list/orgnztList.do?menuNo=400020', 'seoul-jongrogu')) # 여러 링크를 돌아야 되는 듯하다. 하나로는 불가능해 보임.
    print(scrap_basic('https://council.nowon.kr/kr/member/active.do', 'seoul-nowongu'))
    print(scrap_basic('https://council.ep.go.kr/kr/member/name.do', 'seoul-eunpyeonggu'))
    print(scrap_basic('https://www.sdmcouncil.go.kr/source/korean/square/ascending.html', 'seoul-seodaemungu', 'euc-kr'))
    print(scrap_basic('https://council.mapo.seoul.kr/kr/member/active.do', 'seoul-mapogu'))
    # 양천구는 패스
    print(scrap_basic('https://gsc.gangseo.seoul.kr/member/org.asp', 'seoul-gangseogu', 'euc-kr'))
    # 구로구는 링크 터짐
    print(scrap_basic('https://www.ydpc.go.kr/kr/member/active.do', 'seoul-yeongdeungpogu'))