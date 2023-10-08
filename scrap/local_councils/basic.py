from urllib.parse import urlparse

from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
import re
import requests

regex_pattern = re.compile(r'정\s*\S*\s*당', re.IGNORECASE)  # Case-insensitive
party_keywords = ['국민의힘', '더불어민주당', '정의당', '진보당', '기본소득당', '시대전환', '한국의희망', '무소속'] # 이상 원내정당.
# 원외정당의 경우, 나무위키 피셜이지만 현재는 지방의회 진출당이 없다. 사실 당 이름이 매번 바뀌므로 다른 어프로치를 찾아야 할 듯.. => getPartyList() 참고.

pf_elt = [None, 'div']
pf_cls = [None, 'profile']
pf_memlistelt = [None, None]

name_elt = [None, 'em']
name_cls = [None, 'name']
name_wrapelt= [None, None]
name_wrapcls = [None, None]

pty_elt = [None, 'em']
pty_cls = [None, None]
pty_wrapelt = [None, None]
pty_wrapcls = [None, None]

def get_profiles(soup, element, class_, memberlistelement):
    # 의원 목록 사이트에서 의원 프로필을 가져옴
    if memberlistelement is not None:
        soup = soup.find_all(memberlistelement, class_='memberList')[0]
    return soup.find_all(element, class_)

def getDataFromAPI(url_format, data_uid, name_id, party_id) -> Councilor:
    # API로부터 의원 정보를 가져옴
    url = url_format.format(data_uid)
    result = requests.get(url).json()
    return Councilor(name=result[name_id] if result[name_id] else '이름 정보 없음', party=result[party_id] if result[party_id] else '정당 정보 없음')

def get_name(profile, element, class_, wrapper_element, wrapper_class_):
    # 의원 프로필에서 의원 이름을 가져옴
    if wrapper_element is not None:
        profile = profile.find_all(wrapper_element, class_=wrapper_class_)[0]
    name_tag = profile.find(element, class_)
    name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
    if len(name) > 10: # strong태그 등 많은 걸 name 태그 안에 포함하는 경우. 은평구 등.
        name = name_tag.strong.get_text(strip=True) if name_tag.strong else "이름 정보 없음"
    name = name.split('(')[0].split(':')[-1] # 이름 뒷 한자이름, 앞 '이   름:' 제거 

    # 수식어가 이름 뒤에 붙어있는 경우
    while len(name) > 5:
        if name[-3:] in ['부의장']: # 119 등.
            name = name[:-3].strip()
        else:
            break
    while len(name) > 4:
        if name[-2:] in ['의원', '의장']: # 강서구 등.
            name = name[:-2].strip()
        else:
            break # 4자 이름 고려.
    return name

def extract_party(string):
    for keyword in party_keywords:
        if keyword in string:
            return keyword
    return None

def get_party(profile, element, class_, wrapper_element, wrapper_class_, party_in_main_page, url):
    # 의원 프로필에서 의원이 몸담는 정당 이름을 가져옴
    if not party_in_main_page:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        # 프로필보기 링크 가져오기
        profile_link = profile.find('a', class_='start')
        profile_url = base_url + profile_link['href']
        profile = get_soup(profile_url, verify=False)
    party_pulp_list = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all(element, class_)))
    party_pulp = party_pulp_list[0]
    party_string = party_pulp.get_text(strip=True)
    party_string = party_string.split(' ')[-1].strip()
    while True:
        if (party := extract_party(party_string)) is not None:
            return party
        if (party_span := party_pulp.find_next('span')) is not None:
            party_string = party_span.text.split(' ')[-1]
        else:
            return "정당 정보 파싱 불가"

def scrap_basic(url, cid, encoding = 'utf-8') -> ScrapResult:
    '''의원 상세약력 스크랩
    :param url: 의원 목록 사이트 url
    :param n: 의회 id
    :param encoding: 받아온 soup 인코딩
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    soup = get_soup(url, verify=False, encoding=encoding)
    councilors: list[Councilor] = []
    party_in_main_page = any(keyword in soup.text for keyword in party_keywords)
    
    profiles = get_profiles(soup, pf_elt[cid - 1], pf_cls[cid - 1], pf_memlistelt[cid - 1])
    print(cid, '번째 의회에는,', len(profiles), '명의 의원이 있습니다.') # 디버깅용. 

    for profile in profiles:
        name = get_name(profile, name_elt[cid - 1], name_cls[cid - 1], name_wrapelt[cid - 1], name_wrapcls[cid - 1])
        party = get_party(profile, pty_elt[cid - 1], pty_cls[cid - 1], pty_wrapelt[cid - 1], pty_wrapcls[cid - 1], party_in_main_page, url)
            

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=cid,
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_basic('https://02jgnew.council.or.kr/kr/member/active', '2')) # 서울 중구