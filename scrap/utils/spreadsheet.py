import os
import sys
import gspread
import json

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from scrap.local_councils.seoul import *
from scrap.local_councils.busan import *
from scrap.local_councils.daegu import *
from scrap.local_councils.incheon import *
from scrap.local_councils.gwangju import *
# from scrap.local_councils.daejeon import *
from scrap.local_councils.ulsan import *
from scrap.local_councils.gyeonggi import *
from scrap.local_councils.gangwon import *
from scrap.local_councils.chungcheong import *
from scrap.local_councils.jeolla import *
from scrap.local_councils.gyeongsang import *
from scrap.local_councils import *
from requests.exceptions import Timeout

# 구글로부터 권한을 요청할 어플리케이션 목록
# 변경 시 token.json 삭제 후 재인증 필요
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
PWD = os.path.dirname(__file__)
BASE_DIR = os.path.join(PWD, os.pardir, os.pardir)
JSON_PATH = os.path.join(PWD, "scrap_args.json")


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


def read_record_from_spreadsheet() -> list[dict]:
    client = google_authorization()
    link = "https://docs.google.com/spreadsheets/d/1fBDJjkw8FSN5wXrvos9Q2wDsyItkUtNFGOxUZYE-h0M/edit#gid=1127955905"  # T4I-의회목록
    spreadsheet = client.open_by_url(link)
    worksheet = spreadsheet.get_worksheet(0)

    return worksheet.get_all_records()


def main() -> None:
    # TODO - 홈페이지 위 charset=euc-kr 등을 인식해 바로 가져오기.
    euc_kr = [
        6,
        13,
        16,
        31,
        72,
        88,
        112,
        134,
        154,
        157,
        163,
        165,
        167,
        176,
        181,
        197,
        202,
        222,
    ]
    special_functions = (
        list(range(1, 57))
        + [62, 63, 64, 88, 97, 103, 107]
        + list(range(113, 127))
        + [132, 134, 140, 142, 154, 155, 156, 157, 160, 161, 162, 163, 164, 165, 167]
        + list(range(177, 180))
        + [
            182,
            183,
            184,
            186,
            188,
            189,
            190,
            191,
            194,
            195,
            196,
            198,
            199,
            201,
            203,
            206,
            208,
            209,
            210,
        ]
        + list(range(212, 221))
        + [222, 223, 224, 226]
    )
    selenium_basic = [76, 78, 101, 169, 173, 177]
    no_information = [18, 29, 106, 111, 172, 181, 185, 187, 197, 200, 204, 207]
    error_unsolved = [170, 171]
    errors = []
    f = open(JSON_PATH, "r")
    args = json.load(f)
    f.close()

    # 데이터 가져오기
    # data: list[dict] = worksheet.get_all_records()
    data = read_record_from_spreadsheet()
    result: str = ""

    parse_error_times = 0
    timeouts = 0
    N = 226
    for n in range(1, N + 1):  # range(1, N + 1):
        if n in no_information + error_unsolved:
            error_msg = (
                "지난번 확인 시, 정당 정보 등이 홈페이지에 없었습니다. \
            다시 확인해보시겠어요?"
                if n in no_information
                else "함수 구현에 실패한 웹페이지입니다."
            )
            print(f"| {n} | 오류: ", error_msg, " 링크 : ", data[n - 1]["URL"])
            errors.append(n)
            continue
        encoding = "euc-kr" if n in euc_kr else "utf-8"
        council_url: str = ""
        try:
            council_url = data[n - 1]["URL"]
            council_args = args.get(str(n), None)
            if council_args is not None:
                council_args = ScrapBasicArgument(**council_args)
            # council_args = args[n] if n in args.keys() else None

            if n in special_functions:
                function_name = f"scrap_{n}"
                if hasattr(sys.modules[__name__], function_name):
                    function_to_call = getattr(sys.modules[__name__], function_name)  # type: ignore
                    result = str(
                        function_to_call(council_url, n, args=council_args).councilors
                    )
                else:
                    print("[API/spreadsheet] Error : No function found")
            elif n in selenium_basic:
                result = str(sel_scrap_basic(council_url, n, council_args).councilors)
            else:
                result = str(
                    scrap_basic(council_url, n, council_args, encoding).councilors
                )
            if "정보 없음" in result:
                print("정보 없음이 포함되어 있습니다.")
                parse_error_times += 1
                errors.append(n)
            # print(f"| {n} | {result}")
        except Timeout:
            print(f"| {n} | 오류: Request to {council_url} timed out.")
            timeouts += 1
        except Exception as e:
            print(f"| {n} | 오류: {e}")
            errors.append(n)
            continue  # 에러가 발생하면 다음 반복으로 넘어감
    print(
        f"| 총 실행 횟수: {N} | 에러: {errors}, 총 {len(errors)}회 | 그 중 정보 없음 횟수: {parse_error_times} | 타임아웃 횟수: {timeouts} |"
    )


if __name__ == "__main__":
    main()
