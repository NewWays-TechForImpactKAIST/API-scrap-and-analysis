import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread

from scrap.local_councils.seoul import *

# 구글로부터 권한을 요청할 어플리케이션 목록
# 변경 시 token.json 삭제 후 재인증 필요
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def google_authorization():
    '''Google Sheets API 활용을 위한 인증 정보 요청
    credentials.json 파일을 토대로 인증을 요청하되, token.json 파일이 존재할 경우 거기에 저장된 정보 활용
    :todo: credentials.json 파일, token.json 파일 값을 환경변수로 설정
    :return: gspread.client.Client 인스턴스'''

    creds = None

    # 이미 저장된 인증 정보가 있는지 확인
    if os.path.exists('../../_data/token.json'):
        creds = Credentials.from_authorized_user_file('../../_data/token.json', SCOPES)
    
    # 인증 정보가 없거나 비정상적인 경우 인증 재요청
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow= InstalledAppFlow.from_client_secrets_file('../../_data/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('../../_data/token.json', 'w') as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)

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
