"""
각 기초의회들의 크롤링 코드를 모아놓은 패키지입니다.
광역자치단체 별로 폴더를 만들어서 관리합니다.
"""
import re
from urllib.parse import urlparse
from typing import List

from db.types import CouncilType, Councilor
from scrap.utils.types import ScrapResult, ScrapBasicArgument, ArgsType
from scrap.utils.requests import get_soup
from scrap.utils.utils import getPartyList


def ret_local_councilors(cid, councilors):
    return ScrapResult(
        council_id=cid,
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=councilors,
    )
