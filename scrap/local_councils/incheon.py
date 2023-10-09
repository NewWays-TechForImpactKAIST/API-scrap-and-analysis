"""인천광역시를 스크랩. 50-57번째 의회까지 있음.
"""
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
from scrap.local_councils.basic import *

def scrap_50(url='https://www.icjg.go.kr/council/cnmi0101c') -> ScrapResult:
    """인천시 중구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for name_tag in soup.find_all('p', class_='name'):
        name_tag_str = name_tag.get_text(strip=True).split('[')
        name = name_tag_str[0].strip()
        party = name_tag_str[-1][:-1].strip()
        
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="incheon-junggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_51(url='https://council.icdonggu.go.kr/korean/member/active') -> ScrapResult:
    """인천시 동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    raise Exception('현재 인천시 동구의회 사이트는 SSLV3_ALERT_HANDSHAKE_FAILURE 에러가 발생합니다')

    # soup = get_soup(url, verify=False)
    # councilors: list[Councilor] = []

	# # 프로필 링크 스크랩을 위해 base_url 추출
    # parsed_url = urlparse(url)
    # base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # for name_tag in soup.find_all('strong', class_='name'):
    #     name = name_tag.get_text(strip=True)
    #     party = '정당 정보 없음'
        
    #     profile_link = name_tag.find_next('a', class_='abtn1')
    #     if profile_link:
    #         profile_url = base_url + profile_link['onclick'][13:104]
    #         profile_soup = get_soup(profile_url, verify=False)

    #         party_info = profile_soup.find('span', class_='subject', string='소속정당')
    #         if party_info and (party_span := party_info.find_next('span', class_='detail')) is not None:
    #             party = party_span.get_text(strip=True)
        
    #     councilors.append(Councilor(name=name, party=party))

    # return ScrapResult(
    #     council_id="incheon-donggu",
    #     council_type=CouncilType.LOCAL_COUNCIL,
    #     councilors=councilors
    # )


def scrap_52(url='https://www.michuhol.go.kr/council/introduction/career.asp') -> ScrapResult:
    """인천시 미추홀구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []
    
    script = soup.find('div', class_='contents_header').find_next('script').get_text(strip=True)

	# TODO

    return ScrapResult(
        council_id="incheon-michuholgu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_53(url='https://council.yeonsu.go.kr/kr/member/name.do') -> ScrapResult:
    """인천시 연수구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all('div', class_='profile'):
        name_tag = profile.find('strong')
        name = name_tag.get_text(strip=True) if name_tag else '이름 정보 없음'
        
        party = '정당 정보 없음'
        party_info = profile.find('em', string='소속정당').find_next('span').find_next('span')
        if party_info:
            party = party_info.get_text(strip=True)
        
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="incheon-yeonsugu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_54(url='https://council.namdong.go.kr/kr/member/active.do') -> ScrapResult:
    """인천시 남동구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all('div', class_='profile'):
        name_tag = profile.find('em', class_='name')
        name = name_tag.get_text(strip=True) if name_tag else '이름 정보 없음'
        
        party = '정당 정보 없음'
        party_info = profile.find('em', string='정    당 : ').find_next('span')
        if party_info:
            party = party_info.get_text(strip=True)
        
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="incheon-namdonggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )


def scrap_55(url='https://council.icbp.go.kr/kr/member/active') -> ScrapResult:
    """인천시 부평구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    raise Exception('현재 인천시 부평구의회 사이트는 SSLV3_ALERT_HANDSHAKE_FAILURE 에러가 발생합니다')

    # soup = get_soup(url, verify=False)
    # councilors: list[Councilor] = []

    # for profile in soup.find_all('div', class_='profile'):
    #     name_tag = profile.find('strong', class_='name')
    #     name = name_tag.get_text(strip=True).split()[0].strip() if name_tag else '이름 정보 없음'
        
    #     party = '정당 정보 없음'
    #     party_info = profile.find('strong', string='소속정당').find_next('span')
    #     if party_info:
    #         party = party_info.get_text(strip=True).split()[-1].strip()
        
    #     councilors.append(Councilor(name=name, party=party))

    # return ScrapResult(
    #     council_id="incheon-bupyeonggu",
    #     council_type=CouncilType.LOCAL_COUNCIL,
    #     councilors=councilors
    # )


def scrap_56(url='https://www.gyeyang.go.kr/open_content/council/member/present/present.jsp') -> ScrapResult:
    """인천시 계양구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for name_tag in soup.find_all('li', class_='name'):
        name = name_tag.get_text(strip=True) if name_tag else '이름 정보 없음'
        
        party = '정당 정보 없음'
        party_info = name_tag.find_next('li').find_next('li').find('span', class_='span_sfont')
        if party_info:
            party = party_info.get_text(strip=True)
        
        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id="incheon-gyeyanggu",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

def scrap_57(url, args) -> ScrapResult:
    """인천시 서구 페이지에서 의원 상세약력 스크랩

    :param url: 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []
    cid = 57

    profiles = get_profiles(soup, args.pf_elt, args.pf_cls, args.pf_memlistelt, args.pf_memlistcls)
    print(cid, '번째 의회에는,', len(profiles), '명의 의원이 있습니다.') # 디버깅용. 

    for profile in profiles:
        name = get_name(profile, args.name_elt, args.name_cls, args.name_wrapelt, args.name_wrapcls)

        party = '정당 정보 없음'
        party_pulp = profile.find(args.pty_elt, class_=args.pty_cls)
        if party_pulp is None: raise AssertionError('[incheon.py] 정당정보 실패')
        party_string = party_pulp.get_text(strip=True)
        party_string = party_string.split(' ')[-1].strip()
        while True:
            party = extract_party(party_string)
            if party is not None:
                break
            if (party_span := party_pulp.find_next('span')) is not None:
                party_string = party_span.text.split(' ')[-1]
            else:
                raise RuntimeError("[incheon.py] 정당 정보 파싱 불가")

        councilors.append(Councilor(name=name, party=party))

    return ScrapResult(
        council_id=str(cid),
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors
    )

if __name__ == '__main__':
    print(scrap_56())