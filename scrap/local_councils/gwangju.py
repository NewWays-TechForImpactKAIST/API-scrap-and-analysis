"""광주광역시를 스크랩. 60-64번째 의회까지 있음.
"""
from scrap.utils.types import CouncilType, Councilor, ScrapResult
from scrap.utils.requests import get_soup
from scrap.local_councils.basic import *

# def scrap_60(url, args) -> ScrapResult:
#     """인천시 계양구 페이지에서 의원 상세약력 스크랩

#     :param url: 의원 목록 사이트 url
#     :return: 의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
#     """
#     soup = get_soup(url, verify=False)
#     councilors: list[Councilor] = []
#     cid = 57

#     profiles = get_profiles(soup, args.pf_elt, args.pf_cls, args.pf_memlistelt)
#     print(cid, '번째 의회에는,', len(profiles), '명의 의원이 있습니다.') # 디버깅용. 

#     for profile in profiles:
#         name = get_name(profile, args.name_elt, args.name_cls, args.name_wrapelt, args.name_wrapcls)

#         party = '정당 정보 없음'
#         party_pulp = profile.find(args.pty_elt, class_=args.pty_cls)
#         if party_pulp is None: raise AssertionError('[incheon.py] 정당정보 실패')
#         party_string = party_pulp.get_text(strip=True)
#         party_string = party_string.split(' ')[-1].strip()
#         while True:
#             party = extract_party(party_string)
#             if party is not None:
#                 break
#             if (party_span := party_pulp.find_next('span')) is not None:
#                 party_string = party_span.text.split(' ')[-1]
#             else:
#                 raise RuntimeError("[incheon.py] 정당 정보 파싱 불가")

#         councilors.append(Councilor(name=name, party=party))

#     return ScrapResult(
#         council_id=str(cid),
#         council_type=CouncilType.LOCAL_COUNCIL,
#         councilors=councilors
#     )

# if __name__ == '__main__':
#     print(scrap_60())