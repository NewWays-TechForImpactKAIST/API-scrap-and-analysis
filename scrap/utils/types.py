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


class ScrapBasicArgument:
    '''
    scrap_basic에 쓸 argument입니다
    '''
    def __init__(self, pf_elt=None, pf_cls=None, pf_memlistelt=None,
                 name_elt=None, name_cls=None, name_wrapelt=None,
                 name_wrapcls=None, pty_elt=None, pty_cls=None,
                 pty_wrapelt=None, pty_wrapcls=None):
        self.pf_elt = pf_elt
        self.pf_cls = pf_cls
        self.pf_memlistelt = pf_memlistelt
        self.name_elt = name_elt
        self.name_cls = name_cls
        self.name_wrapelt = name_wrapelt
        self.name_wrapcls = name_wrapcls
        self.pty_elt = pty_elt
        self.pty_cls = pty_cls
        self.pty_wrapelt = pty_wrapelt
        self.pty_wrapcls = pty_wrapcls