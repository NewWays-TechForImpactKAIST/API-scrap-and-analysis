import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread

import requests
from bs4 import BeautifulSoup

from urllib.parse import urlparse


# 구글로부터 권한을 요청할 어플리케이션 목록
# 변경 시 token.json 삭제 후 재인증 필요
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# HTTPS 요청에 포함해줄 헤더
HEADERS = {
	"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
}

def google_authorization():
    '''Google Sheets API 활용을 위한 인증 정보 요청
    credentials.json 파일을 토대로 인증을 요청하되, token.json 파일이 존재할 경우 거기에 저장된 정보 활용
    
    :return: gspread.client.Client 인스턴스'''

    creds = None

    # 이미 저장된 인증 정보가 있는지 확인
    if os.path.exists('../_data/token.json'):
        creds = Credentials.from_authorized_user_file('../_data/token.json', SCOPES)
    
    # 인증 정보가 없거나 비정상적인 경우 인증 재요청
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow= InstalledAppFlow.from_client_secrets_file('../_data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('../_data/token.json', 'w') as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)


def scrap_junggu(url):
    '''서울시 중구의회 페이지에서 의원 상세약력 스크랩

    :param url: 중구의회 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 dict의 list
    '''
    
    parliment_response = requests.get(url, verify=False, headers=HEADERS)
    parliment_soup = BeautifulSoup(parliment_response.text, 'html.parser')
    ret = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in parliment_soup.find_all('div', class_='profile'):
        name = profile.find('em', class_='name').text
        party = '정당 정보 없음'

        # 프로필보기 링크 가져오기
        profile_link = profile.find('a', class_='start')
        if profile_link:
            profile_url = base_url + profile_link['href']
            profile_response = requests.get(profile_url, verify=False, headers=HEADERS)
            profile_soup = BeautifulSoup(profile_response.text, 'html.parser')

            party_info = profile_soup.find('em', text='소속정당 : ')
            if party_info:
                party = party_info.find_next('span').string

        ret.append({
            "이름": name,
            "정당": party
        })

    return ret


def scrap_gwangjingu(url):
    '''서울시 광진구 페이지에서 의원 상세약력 스크랩

    :param url: 광진구의회 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 dict의 list
    '''
    
    parliment_response = requests.get(url, verify=False, headers=HEADERS)
    parliment_soup = BeautifulSoup(parliment_response.text, 'html.parser')
    ret = []

    # # 프로필 링크 스크랩을 위해 base_url 추출
    # parsed_url = urlparse(url)
    # base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in parliment_soup.find_all('div', class_='profile'):
        name = profile.find('div', class_='name').find_next('strong').string
        party = '정당 정보 없음'

        party_info = profile.find('em', string = '소속정당')
        if party_info:
            party = party_info.find_next('span').find_next('span').string

        ret.append({
            "이름": name,
            "정당": party
        })

    return ret


def scrap_dongdaemungu(url):
    '''서울시 동대문구 페이지에서 의원 상세약력 스크랩

    :param url: 동대문구의회 의원 목록 사이트 url
    :return: 의원들의 이름과 정당 데이터를 담은 dict의 list
    '''
    
    parliment_response = requests.get(url, verify=False, headers=HEADERS)
    parliment_response.encoding = 'euc-kr'
    parliment_soup = BeautifulSoup(parliment_response.text, 'html.parser')
    ret = []

    # 프로필 링크 스크랩을 위해 base_url 추출
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    for profile in parliment_soup.find_all('div', class_='intro_text tm_lg_6'):
        name = profile.find('p', class_='intro_text_title').string.strip().split(' ')[0]
        party = '정당 정보 없음'

        # 프로필보기 링크 가져오기
        profile_link = profile.find('a')
        if profile_link:
            profile_url = base_url + '/assemblyman/greeting/menu02.asp?assembly_id=' + profile_link['href'][1:]
            profile_response = requests.get(profile_url, verify=False, headers=HEADERS)
            profile_response.encoding = 'euc-kr'
            profile_soup = BeautifulSoup(profile_response.text, 'html.parser')

            profile_info = profile_soup.find('div', class_='profileTxt')
            if profile_info:
                profile_string = profile_info.get_text().strip().split('\xa0')
                idx = profile_string.index('소속정당')
                party = profile_string[idx + 2]

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

    print(scrap_junggu(data[1]['상세약력 링크']))
    print(scrap_gwangjingu(data[4]['상세약력 링크']))
    print(scrap_dongdaemungu(data[5]['상세약력 링크']))


if __name__ == '__main__':
    main()
