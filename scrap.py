import requests
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread
from urllib.parse import urlparse, ParseResult


# 구글로부터 권한을 요청할 어플리케이션 목록
# 변경 시 token.json 삭제 후 재인증 필요
SCOPES: list[str] = ["https://www.googleapis.com/auth/spreadsheets"]
HEADERS: dict = {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}

def google_authorization() -> gspread.client.Client:
    '''Google Sheets API 활용을 위한 인증 정보 요청
    credentials.json 파일을 토대로 인증을 요청하되, token.json 파일이 존재할 경우 거기에 저장된 정보 활용
    
    :return: gspread.client.Client 인스턴스'''

    creds: Credentials = None

    # 이미 저장된 인증 정보가 있는지 확인
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 인증 정보가 없거나 비정상적인 경우 인증 재요청
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow: InstalledAppFlow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)


def scrap_from_site(url: str) -> list[dict]:
    '''주어진 의회 url로부터 의원 상세약력을 스크랩하여 반환
    
    :param url: 의회 사이트의 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 dict의 list
    '''

    print(url)
    parliment_response: requests.Response = requests.get(url, verify=False, headers=HEADERS)
    parliment_soup: BeautifulSoup = BeautifulSoup(parliment_response.text, 'html.parser')
    ret: list[dict] = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url: ParseResult = urlparse(url)
    base_url: str = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in parliment_soup.find_all('div', class_='profile'):
        name: str = profile.find('em', class_='name').text
        party: str = "정당 정보 없음"

        # 프로필보기 링크 가져오기
        profile_link: dict = profile.find('a', class_='start')
        if profile_link:
            profile_url: str = base_url + profile_link['href']
            profile_response: requests.Response = requests.get(profile_url, verify=False, headers=HEADERS)
            profile_soup: BeautifulSoup = BeautifulSoup(profile_response.text, 'html.parser')
            
            # "소속정당" 정보 추출
            party_info = profile_soup.find('em', text='소속정당 : ').find_next('span')
            if party_info:
                party = party_info.string

        ret.append({
            "이름": name,
            "정당": party
        })

    return ret


def main() -> None:
    # Google Sheets API 설정
    client: gspread.client.Client = google_authorization()

    # 스프레드시트 열기
    spreadsheet: gspread.Spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1Eq2x7xZCw_5ng2GdHDnpUIhhwbmOAKEl4abX09JLyuA/edit#gid=1044938838')
    worksheet: gspread.Worksheet = spreadsheet.get_worksheet(1)  # 원하는 워크시트 선택 (0은 첫 번째 워크시트입니다.)

    # 데이터 가져오기
    data: list[dict] = worksheet.get_all_records()

    for tuple in data:
        num_parsed: int = len(scrap_from_site(tuple['상세약력 링크']))
        print(f"{tuple['광역구분']} {tuple['기초자치단체명']}: {num_parsed}")
    # print(scrap_from_site('http://council.ddm.go.kr/citizen/menu1.asp'))


if __name__ == '__main__':
    main()

