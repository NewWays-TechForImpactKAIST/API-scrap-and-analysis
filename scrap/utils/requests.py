"""
크롤링 시 공통적으로 사용하는 requests 라이브러리와 bs4 라이브러리를 사용하기 쉽게 모듈화합니다. 
"""
import requests
from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup

# SSL 인증서 검증 경고 무시
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning) # type: ignore

def get_soup(url: str, additional_headers={}, verify=True, encoding="utf-8") -> BeautifulSoup:
    """
    url을 입력받아 BeautifulSoup 객체를 반환합니다.
    requests 라이브러리를 사용합니다. 크롤링 결과가 정상적으로 나오지 않을 경우, Selenium 라이브러리를 사용할 수 있습니다.
    :param url: 크롤링할 페이지의 url입니다.
    :param additional_headers: 추가적으로 포함할 헤더입니다. 딕셔너리 형태로 입력받습니다.
    :param verify: SSL 인증서 검증 여부입니다. 인증서가 만료된 페이지를 크롤링할 경우 False로 설정합니다.
    :param encoding: 인코딩 설정입니다. 한글이 깨지는 경우 euc-kr 등의 인코딩으로 바꾸어봅니다.
    """

    # HTTP 요청에 포함해줄 헤더
    http_headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
    http_headers.update(additional_headers)
    
    response = requests.get(url, verify=verify, headers=http_headers)
    response.encoding = encoding
    return BeautifulSoup(response.text, 'html.parser')