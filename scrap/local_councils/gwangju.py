"""광주광역시를 스크랩. 60-64번째 의회까지 있음.
"""
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from scrap.local_councils import *

party_keywords = getPartyList()
party_keywords.append("무소속")


def scrap_62(url, cid, args: ArgsType = None) -> ScrapResult:
    """광주 서구"""
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

    councilor_infos = browser.find_elements(By.CSS_SELECTOR, "div[class='con']")
    cur_win = browser.current_window_handle

    for info in councilor_infos:
        name_tag = info.find_element(By.TAG_NAME, "strong")
        name = name_tag.text.strip() if name_tag else "이름 정보 없음"
        homepage_link = info.find_element(By.TAG_NAME, "a")
        homepage_link.click()
        browser.switch_to.window(
            [win for win in browser.window_handles if win != cur_win][0]
        )

        party_tag = browser.find_elements(By.TAG_NAME, "dd")
        party = ""
        for tag in party_tag:
            party = tag.text.strip()
            if party in party_keywords:
                break
        if party not in party_keywords:
            party = "정당 정보 없음"

        browser.close()
        browser.switch_to.window(cur_win)

        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_63(url, cid, args: ArgsType = None) -> ScrapResult:
    """광주 북구"""
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

    councilor_infos = browser.find_elements(By.CSS_SELECTOR, "ul[class='info']")

    for info in councilor_infos:
        name_tag = info.find_element(By.CSS_SELECTOR, "li[class='name']").find_element(
            By.TAG_NAME, "h5"
        )
        name = name_tag.text.strip() if name_tag else "이름 정보 없음"
        party_tag = info.find_elements(By.TAG_NAME, "dd")
        party = ""
        for tag in party_tag:
            party = tag.text.strip()
            if party in party_keywords:
                break
        if party not in party_keywords:
            party = "정당 정보 없음"

        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)


def scrap_64(url, cid, args: ArgsType = None) -> ScrapResult:
    """광주 광산구"""
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

    councilor_infos = browser.find_elements(By.CSS_SELECTOR, "div[class='con']")

    for info in councilor_infos:
        name_tag = info.find_element(By.TAG_NAME, "strong")
        name = name_tag.text.strip() if name_tag else "이름 정보 없음"
        if len(name) > 3:
            # 수식어가 이름 앞이나 뒤에 붙어있는 경우
            for keyword in ["부의장", "의원", "의장"]:  # 119, 강서구 등
                if keyword in name:
                    name = name.replace(keyword, "").strip()
        party_tag = info.find_elements(By.TAG_NAME, "dd")
        party = ""
        for tag in party_tag:
            party = tag.text.replace(" ", "")
            if party in party_keywords:
                break
        if party not in party_keywords:
            party = "정당 정보 없음"

        councilors.append(Councilor(name, party))

    return ret_local_councilors(cid, councilors)
