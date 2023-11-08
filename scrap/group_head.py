"""
광역단체장 및 기초단체장 정보를 스크랩합니다.
"""
from time import sleep

from scrap.utils.types import Councilor
from scrap.utils.requests import get_selenium, By


def scrap_group_heads(
    url="https://laiis.go.kr/lips/mlo/lcl/groupHeadList.do",
) -> tuple[list[tuple[str, Councilor]], list[tuple[str, Councilor]]]:
    """내고장알리미를 이용해 광역/기초단체장 인적사항 스크랩

    :param url: 내고장알리미의 지자체 단체장 목록 사이트
    :return: (광역자치단체, 단체장 정보) 순서쌍의 리스트 2개
    """
    metro_heads: list[tuple[str, Councilor]] = []
    local_heads: list[tuple[str, Councilor]] = []

    browser = get_selenium(url)

    # driver_loc = os.popen("which chromedriver").read().strip()
    # if len(driver_loc) == 0:
    #     raise Exception("ChromeDriver를 다운로드한 후 다시 시도해주세요.")

    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--no-sandbox")

    # webdriver_service = Service(driver_loc)
    # browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    # browser.get(url)

    areas = [
        tag.text.strip()
        for tag in browser.find_element(
            By.CSS_SELECTOR, "div[class='tab_area']"
        ).find_elements(By.TAG_NAME, "a")
    ]

    for area in areas:
        print(area)
        browser.find_element(
            By.CSS_SELECTOR, f"li[data-areaname='{area}']"
        ).find_element(By.TAG_NAME, "a").click()
        sleep(1)

        profiles = browser.find_elements(By.CSS_SELECTOR, "div[class='head_txt_box']")

        metro_head_name_tag = profiles[0].find_element(
            By.CSS_SELECTOR, "p[class='text_align_center fs_18']"
        )
        metro_head_name = (
            metro_head_name_tag.text.strip() if metro_head_name_tag else "이름 정보 없음"
        )
        metro_head_party = "정당 정보 없음"
        metro_heads.append((area, Councilor(metro_head_name, metro_head_party)))

        for profile in profiles[1:]:
            councilor_title = profile.find_element(
                By.CSS_SELECTOR, "p[class='text_align_center fs_14']"
            ).text.strip()
            local_area_name = f"{area} {councilor_title}"

            local_head_name_tag = profile.find_element(
                By.CSS_SELECTOR, "p[class='text_align_center fs_18']"
            )
            local_head_name = (
                local_head_name_tag.text.strip() if local_head_name_tag else "이름 정보 없음"
            )
            local_head_party = "정당 정보 없음"
            local_heads.append(
                (local_area_name, Councilor(local_head_name, local_head_party))
            )

        browser.get(url)

    return (metro_heads, local_heads)


if __name__ == "__main__":
    print(scrap_group_heads())
