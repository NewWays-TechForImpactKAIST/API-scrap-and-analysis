import os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread

from scrap.local_councils.seoul import *
from scrap.local_councils.incheon import *
from scrap.local_councils import *
from requests.exceptions import Timeout

# 구글로부터 권한을 요청할 어플리케이션 목록
# 변경 시 token.json 삭제 후 재인증 필요
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
def google_authorization():
    '''Google Sheets API 활용을 위한 인증 정보 요청
    credentials.json 파일을 토대로 인증을 요청하되, token.json 파일이 존재할 경우 거기에 저장된 정보 활용
    :todo: credentials.json 파일, token.json 파일 값을 환경변수로 설정
    :return: gspread.client.Client 인스턴스'''

    creds = None
    token_json_path = os.path.join(BASE_DIR, '_data', 'token.json')
    # 이미 저장된 인증 정보가 있는지 확인
    if os.path.exists(token_json_path):
        creds = Credentials.from_authorized_user_file(token_json_path, SCOPES)
    
    # 인증 정보가 없거나 비정상적인 경우 인증 재요청
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow= InstalledAppFlow.from_client_secrets_file(os.path.join(BASE_DIR, '_data', 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_json_path, 'w') as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)

def main() -> None:
    # Google Sheets API 설정
    client: gspread.client.Client = google_authorization()

    # 스프레드시트 열기
    link = 'https://docs.google.com/spreadsheets/d/1fBDJjkw8FSN5wXrvos9Q2wDsyItkUtNFGOxUZYE-h0M/edit#gid=1127955905' # T4I-의회목록
    spreadsheet: gspread.Spreadsheet = client.open_by_url(link)
    worksheet: gspread.Worksheet = spreadsheet.get_worksheet(0)  # 원하는 워크시트 선택 (0은 첫 번째 워크시트입니다.)
    euc_kr = [6, 13, 16, 31, 112, 154, 157, 163, 167, 181, 197, 202]
    special_functions = list(range(1, 57)) + [57]
    args = {
        2 : ScrapBasicArgument(pf_elt='div', pf_cls='profile', name_elt='em', name_cls='name',pty_elt='em'),
        3 : ScrapBasicArgument(pf_elt='div', pf_cls='profile', name_elt='em', name_cls='name',pty_elt='em'),
        57 : ScrapBasicArgument(pf_elt='div', pf_cls='box', name_elt='p', name_cls='mem_tit2',pty_elt='p', pty_cls='mem_tit2'),
        113 : ScrapBasicArgument(pf_elt='div', pf_cls='profile', name_cls='name',pty_elt='li'),
        115 : ScrapBasicArgument(pf_elt='div', pf_cls='profile', name_cls='name',pty_elt='li'),
        # TODO : 정당이 주석처리되어 있어서 soup가 인식을 못함.
        116 : ScrapBasicArgument(pf_elt='div', pf_cls='memberName', name_cls='name',pty_elt='dd'),
    }

    # 데이터 가져오기
    data: list[dict] = worksheet.get_all_records()
    result: str = ''

    error_times = 0
    parse_error_times = 0
    timeouts = 0
    N = 226
    # for n in range (113, 169):
    for n in [57]:
        encoding = 'euc-kr' if n in euc_kr else 'utf-8'
        try:
            if n in special_functions:
                function_name = f"scrap_{n}"
                if hasattr(sys.modules[__name__], function_name):
                    function_to_call = getattr(sys.modules[__name__], function_name)
                    if n < 57:
                        result = str(function_to_call(data[n - 1]['상세약력 링크']).councilors)
                    else:
                        result = str(function_to_call(data[n - 1]['상세약력 링크'], args=args[n]).councilors)
            else:
                result = str(scrap_basic(data[n - 1]['상세약력 링크'], n, args[n], encoding).councilors)
            if '정보 없음' in result:
                print("정보 없음이 포함되어 있습니다.")
                parse_error_times += 1
            print(result)
        except Timeout:
            print(f"Request to {data[n - 1]['상세약력 링크']} timed out.")
            timeouts += 1
        except Exception as e:
            print(f"오류 : [district-{n}] {str(e)}")
            error_times += 1
            continue  # 에러가 발생하면 다음 반복으로 넘어감
    print(f"| 총 실행 횟수: {N} | 에러 횟수: {error_times} | 정보 없음 횟수: {parse_error_times} | 타임아웃 횟수: {timeouts} |")
if __name__ == '__main__':
    main()
