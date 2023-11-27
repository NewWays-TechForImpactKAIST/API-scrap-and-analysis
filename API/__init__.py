"""
공공데이터포털 API를 이용한 데이터 수집을 위한 패키지입니다.
"""
import os

from db.types import CouncilType

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)
SG_TYPECODE = {
    "0": "대표선거명",
    "1": "대통령",
    "2": "국회의원",
    "3": "시도지사",
    "4": "구시군장",
    "5": "시도의원",
    "6": "구시군의회의원",
    "7": "국회의원비례대표",
    "8": "광역의원비례대표",
    "9": "기초의원비례대표",
    "10": "교육의원",
    "11": "교육감",
}
ELECTED_TYPECODE_TYPE = {
    "2": CouncilType.NATIONAL_COUNCIL,
    "3": CouncilType.METRO_LEADER,
    "4": CouncilType.LOCAL_LEADER,
    "5": CouncilType.METROPOLITAN_COUNCIL,
    "6": CouncilType.LOCAL_COUNCIL,
    "8": CouncilType.METROPOLITAN_COUNCIL,
    "9": CouncilType.LOCAL_COUNCIL,
}
CANDIDATE_TYPECODE_TYPE = {
    "2": CouncilType.NATIONAL_COUNCIL_CAND,
    "5": CouncilType.METROPOLITAN_COUNCIL_CAND,
    "6": CouncilType.LOCAL_COUNCIL_CAND,
    "9": CouncilType.LOCAL_COUNCIL_CAND,
}
