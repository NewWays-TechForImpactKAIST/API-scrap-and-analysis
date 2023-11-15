# coding: utf-8
"""
의회 크롤링 결과를 나타내는 타입을 정의합니다.
"""
from typing import Optional, List
from dataclasses import dataclass
from db.types import CouncilType, Councilor


@dataclass
class ScrapResult:
    """
    의회 크롤링 결과를 나타내는 타입입니다.
    """

    council_id: int
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
    """
    scrap_basic에 쓸 argument입니다
    """

    def __init__(
        self,
        pf_elt: str | None = None,
        pf_cls: str | None = None,
        pf_memlistelt: str | None = None,
        pf_memlistcls: str | None = None,
        name_elt: str | None = None,
        name_cls: str | None = None,
        name_wrapelt: str | None = None,
        name_wrapcls: str | None = None,
        pty_elt: str | None = None,
        pty_cls: str | None = None,
        pty_wrapelt: str | None = None,
        pty_wrapcls: str | None = None,
        pty_wraptxt: str | None = None,
    ):
        """
        ScrapBasicArgument 클래스의 생성자입니다.

        Args:
            - pf_elt (str | None): pf의 요소 이름. 일반적으로 'div'입니다.
            - pf_cls (str | None): pf의 클래스 이름. 일반적으로 'profile'입니다.
            - pf_memlistelt (str | None): pf 멤버 목록 요소 이름.
            - pf_memlistelt (str | None): pf 멤버 목록 클래스 이름.
            - name_elt (str | None): 이름 요소의 이름. 존재한다면 일반적으로 'em'입니다.
            - name_cls (str | None): 이름 요소의 클래스 이름. 일반적으로 'name'입니다.
            - name_wrapelt (str | None): 이름 래퍼 요소의 이름.
            - name_wrapcls (str | None): 이름 래퍼 요소의 클래스 이름.
            - pty_elt (str | None): 속성 요소의 이름.
            - pty_cls (str | None): 속성 요소의 클래스 이름.
            - pty_wrapelt (str | None): 속성 래퍼 요소의 이름. 존재한다면 일반적으로 'a'입니다.
            - pty_wrapcls (str | None): 속성 래퍼 요소의 클래스 이름. 존재한다면 일반적으로 'start'입니다.
            - pty_wraptxt (str | None): 속성 래퍼 요소의 텍스트.
        """
        self.pf_elt = pf_elt
        self.pf_cls = pf_cls
        self.pf_memlistelt = pf_memlistelt
        self.pf_memlistcls = pf_memlistcls
        self.name_elt = name_elt
        self.name_cls = name_cls
        self.name_wrapelt = name_wrapelt
        self.name_wrapcls = name_wrapcls
        self.pty_elt = pty_elt
        self.pty_cls = pty_cls
        self.pty_wrapelt = pty_wrapelt
        self.pty_wrapcls = pty_wrapcls
        self.pty_wraptxt = pty_wraptxt


ArgsType = Optional[ScrapBasicArgument]
