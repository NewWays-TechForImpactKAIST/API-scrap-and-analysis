#coding: utf-8
"""
의회 크롤링 결과를 나타내는 타입을 정의합니다.
"""
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass

class CouncilType(str, Enum):
    """
    의회의 종류를 나타내는 열거형입니다.
    """
    LOCAL_COUNCIL = "local_council" 
    NATIONAL_COUNCIL = "national_council"
    METROPOLITAN_COUNCIL = "metropolitan_council"
    """
    기초의회
    """
    def __str__(self):
        """
        JSON으로 직렬화하기 위해 문자열로 변환하는 함수를 오버라이드합니다.
        """
        return str(self.value)

@dataclass
class Councilor:
    """
    의원(이름 및 정당)을 나타내는 타입입니다.
    """
    name: str
    party: str

@dataclass
class ScrapResult:
    """
    의회 크롤링 결과를 나타내는 타입입니다.
    """
    council_id: str
    """
    의회를 구분하기 위한 문자열입니다.
    """
    council_type: CouncilType
    """
    의회의 종류를 나타내는 문자열입니다.
    """
    councilors: Optional[List[Councilor]]
    """
    의회 의원 목록입니다.
    """


