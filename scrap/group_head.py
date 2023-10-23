from scrap.utils.types import CouncilType, Councilor, ScrapResult
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep


def scrap_metro_head(
    metropolis,
    url="https://laiis.go.kr/lips/mlo/lcl/groupHeadList.do",
) -> ScrapResult:
    """내고장알리미를 이용해 광역단체장 인적사항 스크랩

    :param metropolis: 특별시, 광역시, 혹은 도
    :param url: 내고장알리미의 지자체 단체장 목록 사이트
    :return: 국회의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    webdriver_service = Service("/usr/bin/chromedriver")
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    browser.get(url)

    link = browser.find_element(
        By.CSS_SELECTOR, f'li[data-areaname="{metropolis}"]'
    ).find_element(By.TAG_NAME, "a")
    link.click()
    sleep(3)

    profile = browser.find_element(By.CSS_SELECTOR, "div[class='head_txt_box']")
    name_tag = profile.find_element(
        By.CSS_SELECTOR, "p[class='text_align_center fs_18']"
    )
    name = name_tag.text.strip() if name_tag else "이름 정보 없음"
    party = "정당 정보 없음"

    browser.quit()
    return ScrapResult(
        council_id=metropolis,
        council_type=CouncilType.LOCAL_LEADER,
        councilors=[Councilor(name=name, party=party)],
    )


def scrap_local_head(
    metropolis,
    town,
    url="https://laiis.go.kr/lips/mlo/lcl/groupHeadList.do",
) -> ScrapResult:
    """내고장알리미를 이용해 기초단체장 인적사항 스크랩

    :param metropolis: 특별시, 광역시, 혹은 도
    :param town: 시, 군, 구
    :param url: 내고장알리미의 지자체 단체장 목록 사이트
    :return: 국회의원들의 이름과 정당 데이터를 담은 ScrapResult 객체
    """

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    webdriver_service = Service("/usr/bin/chromedriver")
    browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    browser.get(url)

    link = browser.find_element(
        By.CSS_SELECTOR, f'li[data-areaname="{metropolis}"]'
    ).find_element(By.TAG_NAME, "a")
    link.click()
    sleep(3)

    for profile in browser.find_elements(By.CSS_SELECTOR, "div[class='head_txt_box']"):
        if profile.find_element(
            By.CSS_SELECTOR, "p[class='text_align_center fs_14']"
        ).text.startswith(town):
            name_tag = profile.find_element(
                By.CSS_SELECTOR, "p[class='text_align_center fs_18']"
            )
            name = name_tag.text.strip() if name_tag else "이름 정보 없음"
            party = "정당 정보 없음"

            browser.quit()
            return ScrapResult(
                council_id=metropolis + " " + town,
                council_type=CouncilType.LOCAL_LEADER,
                councilors=[Councilor(name=name, party=party)],
            )

    browser.quit()
    raise Exception(f"{metropolis} {town}의 기초의회장을 찾지 못했습니다")


if __name__ == "__main__":
    print(scrap_metro_head("서울"))
    print(scrap_local_head("서울", "종로구"))
