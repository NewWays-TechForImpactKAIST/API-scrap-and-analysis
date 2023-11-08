import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from scrap.utils.types import Councilor, ScrapResult, ScrapBasicArgument
from scrap.utils.requests import get_soup
from scrap.local_councils.basic import *
from scrap.utils.utils import getPartyList

party_keywords = getPartyList()
party_keywords.append("무소속")


def scrap_107(
    url, cid,
) -> ScrapResult:
    """강원도 원주시
    """
    councilors: list[Councilor] = []

    driver_loc = os.popen("which chromedriver").read().strip()
    if len(driver_loc) == 0:
        raise Exception("ChromeDriver를 다운로드한 후 다시 시도해주세요.")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    webdriver_service = Service(driver_loc)
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    browser.get(url)

    pfs_wrapper = browser.find_element(By.CSS_SELECTOR, "div[id='content']")
    councilor_infos = pfs_wrapper.find_elements(By.CSS_SELECTOR, "dl")
    for info in councilor_infos:
        name_tag = info.find_element(By.CSS_SELECTOR, "dd[class='name']")
        name = name_tag.text.split("(")[0].strip() if name_tag else "이름 정보 없음"
        if len(name) > 3:
            # 수식어가 이름 앞이나 뒤에 붙어있는 경우
            for keyword in ["부의장", "의원", "의장"]:  # 119, 강서구 등
                if keyword in name:
                    name = name.replace(keyword, "").strip()
        party_tag = info.find_elements(By.TAG_NAME, "dd")
        for tag in party_tag:
            party = tag.text.split(" ")[-1]
            if party in party_keywords:
                break
        if party not in party_keywords:
            party = "정당 정보 없음"

        councilors.append(Councilor(name, party))

    return returncouncilors(cid, councilors)


def scrap_113(
    url, cid, args: ScrapBasicArgument = None
) -> ScrapResult:
    """강원도 속초시
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("em", class_="name")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_tags = profile.find_all("li")
        for tag in party_tags:
            if "소속정당" in tag.get_text():
                party = tag.find("span").get_text(strip=True)
                break

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_114(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 고성군
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("li", class_="list-item"):
        name_tag = profile.find("div", class_="list-content").find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"
        if not name:
            break

        party = "정당 정보 없음"
        dd_tags = profile.find_all("dd")
        for tag in dd_tags:
            if "소속정당" in tag.get_text():
                party = tag.find("strong").get_text(strip=True)
                break

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_115(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 양양군
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.find("div", class_="name").find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        li_tags = profile.find_all("li")
        for tag in li_tags:
            if "소속정당" in tag.get_text():
                party = tag.find("span").find_next().get_text(strip=True)
                break

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_116(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 인제군
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("dl"):
        name_tag = profile.find("dd", class_="name").find("strong")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_117(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 홍천군
    """
    soup = get_soup(url, verify=False, encoding="euc-kr")
    councilors: list[Councilor] = []

    for profile in soup.find_all("ul", class_="box"):
        name_tag = profile.find("p", class_="b1_title")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        li_tags = profile.find("ul", class_="b2_icon").find_all("li")
        for tag in li_tags:
            if "소속정당" in tag.get_text():
                span_text = tag.find("span").get_text(strip=True)
                party = tag.get_text(strip=True).replace(span_text, "").strip()
                break

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_118(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 횡성군
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="person_info"):
        name_td = profile.find("th", string="성함/직위").find_next("td")
        name = name_td.get_text(strip=True) if name_td else "이름 정보 없음"

        party_td = profile.find("th", string="정당").find_next("td")
        party = party_td.get_text(strip=True) if party_td else "정당 정보 없음"

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_119(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 영월군
    """
    base_url = "https://council.yw.go.kr"
    soup = get_soup(url)
    councilors: list[Councilor] = []

    # 1. 의원별 누리집 링크 추출
    member_links = [
        base_url + link["href"] for link in soup.select("li.member ul li a")
    ]

    # 2. 각 링크 접속 후 정당 정보 추출
    for link in member_links:
        member_soup = get_soup(link)
        name = "이름 정보 없음"
        party = "정당 정보 없음"

        name = member_soup.select_one("div.main_w1 h3").text.split("(")[0].strip()
        party = (
            member_soup.select_one("li:contains('소속정당')")
            .text.replace("소속정당:", "")
            .strip()
        )

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_120(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 평창군
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="profile"):
        name_tag = profile.select_one(".name")
        name = name_tag.text.split("(")[0].strip() if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        party_tag = profile.select_one("li:contains('소속정당')")
        if party_tag:
            party = party_tag.select_one("span").text.strip()

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_121(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 화천군
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("ul", class_="sub01_06_ul2"):
        name_tag = profile.select_one(".sub_title")
        name = name_tag.get_text(strip=True).split()[0] if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_122(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 양구군
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="person_pop_wrap"):
        name_tag = profile.find("h2", class_="tit")
        name = name_tag.get_text(strip=True) if name_tag else "이름 정보 없음"

        party = "정당 정보 없음"
        # TODO

        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


def scrap_123(
    url, cid,
    args: ScrapBasicArgument = None,
) -> ScrapResult:
    """강원도 철원군
    """
    soup = get_soup(url, verify=False)
    councilors: list[Councilor] = []

    for profile in soup.find_all("div", class_="img_text_box"):
        name_li = profile.select_one("ul.bu li:contains('성명')")
        name = (
            name_li.get_text(strip=True).replace("성명", "").strip()
            if name_li
            else "이름 정보 없음"
        )

        party = "정당 정보 없음"
        # TODO
        councilors.append(Councilor(name=name, party=party))

    return returncouncilors(cid, councilors)


if __name__ == "__main__":
    print(scrap_123())
