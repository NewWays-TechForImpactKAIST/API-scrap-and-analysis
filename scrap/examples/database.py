"""
서울시의 세 의회의 크롤링 결과를 데이터베이스에 저장하는 예제입니다.
"""

from scrap.utils.database import save_to_database
from scrap.local_councils.seoul import (
    scrap_dongdaemungu,
    scrap_gwangjingu,
    scrap_junggu,
)


def main() -> None:
    # 서울시 동대문구의회 크롤링 결과를 데이터베이스에 저장합니다.
    save_to_database(scrap_dongdaemungu())
    # 서울시 광진구의회 크롤링 결과를 데이터베이스에 저장합니다.
    save_to_database(scrap_gwangjingu())
    # 서울시 중구의회 크롤링 결과를 데이터베이스에 저장합니다.
    save_to_database(scrap_junggu())


if __name__ == "__main__":
    main()
