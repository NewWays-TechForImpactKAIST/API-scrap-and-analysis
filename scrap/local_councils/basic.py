from urllib.parse import urlparse

from scrap.utils.types import CouncilType, Councilor, ScrapResult, ScrapBasicArgument
from scrap.utils.requests import get_soup
from scrap.utils.utils import getPartyList
import re
import requests

regex_pattern = re.compile(r'정\s*\S*\s*당', re.IGNORECASE)  # Case-insensitive
party_keywords = getPartyList()
party_keywords.append('무소속')

def get_profiles(soup, element, class_, memberlistelement, memberlistclass_):
    # 의원 목록 사이트에서 의원 프로필을 가져옴
    if memberlistelement is not None:
        try:
            soup = soup.find_all(memberlistelement, class_=memberlistclass_)[0]
        except Exception:
            raise RuntimeError('[basic.py] 의원 목록 사이트에서 의원 프로필을 가져오는데 실패했습니다.') 
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
    # strong태그 등 많은 걸 name 태그 안에 포함하는 경우. 은평구 등.
    # 울산 동구의 이름름(한자자)(의장) 은 10자를 넘는다. 15가 좋은 기준.
    if len(name) > 15:
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
        elif any(keyword in name for keyword in party_keywords): 
            # 인천 서구 등. 정당 키워드는 제거해야 함 
            for keyword in party_keywords:
                if keyword in name:
                    name = name.replace(keyword, '').strip()
                    break
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
        profile_link = profile.find(wrapper_element, class_=wrapper_class_)
        profile_url = base_url + profile_link['href']
        profile = get_soup(profile_url, verify=False)
    party_pulp_list = list(filter(lambda x: regex_pattern.search(str(x)), profile.find_all(element, class_)))
    if party_pulp_list == []: raise RuntimeError('[basic.py] 정당정보 regex 실패')
    party_pulp = party_pulp_list[0]
    party_string = party_pulp.get_text(strip=True)
    party_string = party_string.strip().split(' ')[-1]
    while True:
        if (party := extract_party(party_string)) is not None:
            return party
        if (party_pulp := party_pulp.find_next('span')) is not None:
            party_string = party_pulp.text.strip().split(' ')[-1]
        else:
            return "[basic.py] 정당 정보 파싱 불가"

def scrap_basic(url, cid, args: ScrapBasicArgument, encoding = 'utf-8') -> ScrapResult:
    '''의원 상세약력 스크랩
    :param url: 의원 목록 사이트 url
    :param n: 의회 id
    :param encoding: 받아온 soup 인코딩
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    '''
    soup = get_soup(url, verify=False, encoding=encoding)
    councilors: list[Councilor] = []
    party_in_main_page = any(keyword in soup.text for keyword in party_keywords)
    print(soup)
    profiles = get_profiles(soup, args.pf_elt, args.pf_cls, args.pf_memlistelt, args.pf_memlistcls)
    print(cid, '번째 의회에는,', len(profiles), '명의 의원이 있습니다.') # 디버깅용. 

    for profile in profiles:
        name = get_name(profile, args.name_elt, args.name_cls, args.name_wrapelt, args.name_wrapcls)
        party = get_party(profile, args.pty_elt, args.pty_cls, args.pty_wrapelt, args.pty_wrapcls, party_in_main_page, url)

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(cid),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    args3 = ScrapBasicArgument(pf_elt='div', pf_cls='profile', name_elt='em',name_cls='name',pty_elt='em')
    print(scrap_basic('https://www.yscl.go.kr/kr/member/name.do', 3, args3)) # 서울 용산구 