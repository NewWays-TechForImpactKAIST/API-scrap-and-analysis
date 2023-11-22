# coding: utf-8
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass


class CouncilType(str, Enum):
    """
    의회의 종류를 나타내는 열거형입니다.
    """

    LOCAL_COUNCIL = "local_councilor"
    NATIONAL_COUNCIL = "national_councilor"
    METROPOLITAN_COUNCIL = "metropolitan_councilor"
    LOCAL_LEADER = "local_leader"
    METRO_LEADER = "metro_leader"
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
    jdName: str
