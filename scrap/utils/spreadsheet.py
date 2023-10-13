import os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread

from scrap.local_councils.seoul import *
from scrap.local_councils import *
from requests.exceptions import Timeout

# 구글로부터 권한을 요청할 어플리케이션 목록
# 변경 시 token.json 삭제 후 재인증 필요
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)


def google_authorization():
    """Google Sheets API 활용을 위한 인증 정보 요청
    credentials.json 파일을 토대로 인증을 요청하되, token.json 파일이 존재할 경우 거기에 저장된 정보 활용
    :todo: credentials.json 파일, token.json 파일 값을 환경변수로 설정
    :return: gspread.client.Client 인스턴스"""

    creds = None
    token_json_path = os.path.join(BASE_DIR, "_data", "token.json")
    # 이미 저장된 인증 정보가 있는지 확인
    if os.path.exists(token_json_path):
        creds = Credentials.from_authorized_user_file(token_json_path, SCOPES)

    # 인증 정보가 없거나 비정상적인 경우 인증 재요청
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(BASE_DIR, "_data", "credentials.json"), SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open(token_json_path, "w") as token:
            token.write(creds.to_json())

    return gspread.authorize(creds)


def main() -> None:
    # Google Sheets API 설정
    client: gspread.client.Client = google_authorization()

    # 스프레드시트 열기
    spreadsheet: gspread.Spreadsheet = client.open_by_url(
        "https://docs.google.com/spreadsheets/d/1Eq2x7xZCw_5ng2GdHDnpUIhhwbmOAKEl4abX09JLyuA/edit#gid=1044938838"
    )
    worksheet: gspread.Worksheet = spreadsheet.get_worksheet(
        1
    )  # 원하는 워크시트 선택 (0은 첫 번째 워크시트입니다.)

    # 데이터 가져오기
    data: list[dict] = worksheet.get_all_records()

    print(scrap_junggu(data[1]["상세약력 링크"]))
    print(scrap_gwangjingu(data[4]["상세약력 링크"]))
    print(scrap_dongdaemungu(data[5]["상세약력 링크"]))
    for n in range(65, 75):
        function_name = f"scrap_{n}"
        if hasattr(sys.modules[__name__], function_name):
            function_to_call = getattr(sys.modules[__name__], function_name)
            print(function_to_call)
            if n in [66, 70, 74]:
                result = function_to_call()  # 스프레드시트 링크 터짐 (울산 울주군처럼 애먼데 링크인 경우도 있다)
            else:
                result = function_to_call(data[n - 1]["상세약력 링크"])
            print(result)
        else:
            print(f"함수 {function_name}를 찾을 수 없습니다.")

    ## 아래 테스트를 위해서는 위 프린트문을 모두 주석처리해 주세요.
    # error_times = 0
    # parse_error_times = 0
    # timeouts = 0
    # N = 226
    # for n in range (N):
    #     encoding = 'euc-kr' if n in [5, 12, 15, 30, 111, 153, 156, 162, 166, 180, 196, 201] else 'utf-8'
    #     try:
    #         result = str(scrap_basic(data[n]['상세약력 링크'], f'district-{n}', encoding))
    #         if '정보 없음' in result:
    #             print("정보 없음이 포함되어 있습니다.")
    #             parse_error_times += 1
    #         print(result)
    #     except Timeout:
    #         print(f"Request to {data[n]['상세약력 링크']} timed out.")
    #         timeouts += 1
    #     except Exception as e:
    #         print(f"An error occurred for district-{n}: {str(e)}")
    #         error_times += 1
    #         continue  # 에러가 발생하면 다음 반복으로 넘어감
    # print(f"| 총 실행 횟수: {N} | 에러 횟수: {error_times} | 정보 없음 횟수: {parse_error_times} | 타임아웃 횟수: {timeouts} |")


if __name__ == "__main__":
    main()
