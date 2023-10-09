from urllib.parse import urlparse
import re

from scrap.utils.types import CouncilType, Councilor, ScrapResult, ScrapBasicArgument
from scrap.utils.requests import get_soup
from scrap.local_councils.basic import scrap_basic
