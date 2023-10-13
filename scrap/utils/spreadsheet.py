import os, sys
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import gspread

from scrap.local_councils.seoul import *
from scrap.local_councils.incheon import *
from scrap.local_councils.gwangju import *
from scrap.local_councils.gyeonggi import *
from scrap.local_councils.gangwon import *
from scrap.local_councils.chungcheong import *
from scrap.local_councils.jeolla import *
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
    link = "https://docs.google.com/spreadsheets/d/1fBDJjkw8FSN5wXrvos9Q2wDsyItkUtNFGOxUZYE-h0M/edit#gid=1127955905"  # T4I-의회목록
    spreadsheet: gspread.Spreadsheet = client.open_by_url(link)
    worksheet: gspread.Worksheet = spreadsheet.get_worksheet(
        0
    )  # 원하는 워크시트 선택 (0은 첫 번째 워크시트입니다.)
    # TODO - 홈페이지 위 charset=euc-kr 등을 인식해 바로 가져오기.
    euc_kr = [6, 13, 16, 31, 72, 88, 112, 134, 154, 157, 163, 165, 167, 181, 197, 202]
    special_functions = (
        list(range(1, 57))
        + [57, 88, 103]
        + list(range(113, 127))
        + [132, 134, 140, 142, 154, 155, 156, 157, 160, 161, 162, 163, 164, 165, 167]
    )
    args = {
        2: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        3: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        # 인천
        57: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="box",
            name_elt="p",
            name_cls="mem_tit2",
            pty_elt="p",
            pty_cls="mem_tit2",
        ),
        58: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        59: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_elt="em",
        ),
        # 광주
        60: ScrapBasicArgument(
            pf_elt="div", pf_cls="content", name_elt="h5", pty_wrapelt="a", pty_elt="li"
        ),
        61: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        # 62 : TODO! /common/selectCouncilMemberProfile.json 을 어떻게 얻을지..
        # 63 : TODO! 홈페이지 터짐
        # 64 : TODO! /common/selectCouncilMemberProfile.json 을 어떻게 얻을지..
        # 대전
        65: ScrapBasicArgument(
            pf_elt="dl",
            pf_cls="profile",
            name_elt="strong",
            name_cls="name",
            pty_elt="strong",
        ),
        66: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_elt="em",
        ),
        67: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="member",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="dd",
        ),
        68: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        69: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        # 울산
        70: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="memberName",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="dd",
        ),
        71: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="memberName",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="dd",
        ),
        72: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="li", name_cls="name", pty_elt="li"
        ),
        73: ScrapBasicArgument(
            pf_elt="dl",
            pf_cls="profile",
            name_elt="strong",
            name_cls="name",
            pty_elt="li",
        ),
        74: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_wrapelt="a",
            pty_wrapcls="start",
            pty_elt="li",
        ),
        # 경기
        75: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_elt="em",
        ),
        76: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        77: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="mbrListByName",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="dd",
        ),
        78: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_wrapelt="a",
            pty_wrapcls="end",
            pty_elt="li",
        ),
        79: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        80: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        81: ScrapBasicArgument(
            pf_memlistelt="div",
            pf_memlistcls="member_list",
            pf_elt="dd",
            name_elt="p",
            pty_elt="tr",
        ),
        82: ScrapBasicArgument(
            pf_memlistelt="div",
            pf_memlistcls="cts1426_box",
            pf_elt="div",
            pf_cls="conbox",
            name_elt="p",
            pty_elt="li",
        ),
        # 경기 - 동두천
        83: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_wrapelt="a",
            pty_wrapcls="start",
            pty_elt="li",
        ),
        84: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="law_box",
            name_elt="span",
            name_cls="name",
            pty_elt="p",
        ),
        85: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_elt="em",
        ),
        86: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        87: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        88: ScrapBasicArgument(
            pf_memlistelt="div",
            pf_memlistcls="member_list",
            pf_elt="dl",
            pf_cls="box",
            name_elt="span",
            name_cls="name",
            pty_wrapelt="p",
            pty_wrapcls="btn",
            pty_elt="li",
        ),
        89: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="memberName",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
        ),
        90: ScrapBasicArgument(
            pf_elt="dl",
            pf_cls="profile",
            name_elt="strong",
            name_cls="name",
            pty_elt="li",
        ),
        # 경기 - 화성
        91: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="mbr0101",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="dd",
        ),
        92: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="member",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="dd",
        ),
        93: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_wrapelt="a",
            pty_wrapcls="end",
            pty_elt="li",
        ),
        94: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="mbrListByName",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="dd",
        ),
        95: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="member",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="tr",
        ),
        96: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_elt="em",
        ),
        97: ScrapBasicArgument(
            pf_memlistelt="ul",
            pf_memlistcls="memberList",
            pf_elt="li",
            name_elt="strong",
            pty_wrapelt="a",
            pty_elt="tr",
        ),
        98: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        99: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        100: ScrapBasicArgument(
            pf_elt="div", pf_cls="list", name_elt="h4", name_cls="h0", pty_elt="li"
        ),
        # 경기 - 광주
        101: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        102: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_wrapelt="a",
            pty_wrapcls="start",
            pty_elt="li",
        ),
        103: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="col-sm-6",
            name_elt="h5",
            name_cls="h5",
            pty_wrapelt="a",
            pty_wrapcls="d-inline-block",
            pty_elt="li",
        ),
        104: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="text_box",
            name_elt="h3",
            name_cls="h0",
            pty_wrapelt="a",
            pty_wraptxt="누리집",
            pty_elt="li",
        ),
        105: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        # 강원
        # 106 : TODO! 정당정보 없음
        # TODO! 107이 get_soup에서 실패 중 - HTTPSConnectionPool(host='council.wonju.go.kr', port=443): Max retries exceeded with url: /content/member/memberName.html (Caused by SSLError(SSLError(1, '[SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:1007)')))
        107: ScrapBasicArgument(
            pf_memlistelt="div",
            pf_memlistcls="content",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
        ),
        108: ScrapBasicArgument(
            pf_elt="dl", pf_cls="profile", name_elt="strong", pty_elt="li"
        ),
        109: ScrapBasicArgument(
            pf_memlistelt="section",
            pf_memlistcls="memberName",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
        ),
        110: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        # 111 : TODO! 정당 없고 홈페이지는 깨짐
        112: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_elt="em", name_cls="name", pty_elt="em"
        ),
        113: ScrapBasicArgument(
            pf_elt="div", pf_cls="profile", name_cls="name", pty_elt="li"
        ),
        115: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_elt="li",
        ),
        # TODO : 정당이 주석처리되어 있어서 soup가 인식을 못함.
        116: ScrapBasicArgument(
            pf_elt="div", pf_cls="memberName", name_cls="name", pty_elt="dd"
        ),
        127: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_elt="span",
        ),
        128: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_elt="span",
        ),
        129: ScrapBasicArgument(
            pf_memlistelt="ul",
            pf_memlistcls="memberList",
            pf_elt="div",
            pf_cls="right",
            name_elt="h5",
            pty_elt="span",
        ),
        130: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="parliament_text",
            name_elt="h3",
            name_cls="h0",
            pty_elt="span",
        ),
        131: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_elt="span",
        ),
        133: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="div",
            name_cls="name",
            pty_elt="span",
        ),
        135: ScrapBasicArgument(
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
            pty_cls="itemContent",
        ),
        136: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="info",
            name_elt="div",
            name_cls="tit",
            pty_elt="li",
        ),
        137: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_elt="span",
        ),
        138: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="item",
            name_elt="h5",
            name_cls="name",
            pty_elt="span",
        ),
        # TODO: 139 크롤링 실패
        # HTTPSConnectionPool(host='www.scc.go.kr', port=443): Max retries exceeded with url: /index.php?MenuID=48 (Caused by SSLError(SSLError(1, '[SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:1007)')))
        139: ScrapBasicArgument(
            pf_elt="ul",
            pf_cls="assembly_list",
            name_elt="div",
            name_cls="names",
            pty_elt="li",
        ),
        141: ScrapBasicArgument(
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
            pty_cls="itemContent",
        ),
        143: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="card--body",
            name_elt="strong",
            name_cls="ui-list__title",
            pty_elt="li",
        ),
        # TODO: 144 크롤링 실패
        # HTTPSConnectionPool(host='council.dangjin.go.kr', port=443): Max retries exceeded with url: /content/member/member.html (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1007)')))
        144: ScrapBasicArgument(
            pf_memlistelt="ul",
            pf_memlistcls="mlist",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
            pty_cls="itemContent",
        ),
        # TODO: 145 크롤링 실패
        # HTTPSConnectionPool(host='council.buyeo.go.kr', port=443): Max retries exceeded with url: /kr/member/active2.do (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure (_ssl.c:1007)')))
        145: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_elt="span",
        ),
        # TODO: 146 크롤링 실패
        # HTTPSConnectionPool(host='www.scouncil.go.kr', port=443): Max retries exceeded with url: /kr/prog/asemby/sub02_01/list.do (Caused by SSLError(SSLError(1, '[SSL: WRONG_SIGNATURE_TYPE] wrong signature type (_ssl.c:1007)')))
        146: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="pt",
            name_elt="strong",
            name_cls="name",
            pty_elt="li",
        ),
        147: ScrapBasicArgument(
            pf_elt="dl",
            pf_cls="profile",
            name_elt="strong",
            name_cls="name",
            pty_elt="span",
        ),
        148: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="col",
            name_elt="strong",
            name_cls="ui-list__title",
            pty_elt="li",
        ),
        149: ScrapBasicArgument(
            pf_elt="dl",
            pf_cls="profile",
            name_elt="strong",
            name_cls="name",
            pty_elt="span",
        ),
        150: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="strong",
            name_cls="name",
            pty_elt="span",
        ),
        151: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_elt="span",
        ),
        152: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="councillor_info",
            name_elt="span",
            name_cls="name",
            pty_elt="li",
        ),
        153: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="em",
            name_cls="name",
            pty_elt="span",
        ),
        158: ScrapBasicArgument(
            pf_memlistelt="ul",
            pf_memlistcls="mlist",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
            pty_cls="itemContent",
        ),
        159: ScrapBasicArgument(
            pf_memlistelt="ul",
            pf_memlistcls="mlist",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
            pty_cls="itemContent",
        ),
        166: ScrapBasicArgument(
            pf_elt="div",
            pf_cls="profile",
            name_elt="strong",
            pty_elt="span",
        ),
        168: ScrapBasicArgument(
            pf_memlistelt="ul",
            pf_memlistcls="mlist",
            pf_elt="dl",
            name_elt="dd",
            name_cls="name",
            pty_elt="span",
            pty_cls="itemContent",
        ),
    }

    # 데이터 가져오기
    data: list[dict] = worksheet.get_all_records()
    result: str = ""

    error_times = 0
    parse_error_times = 0
    timeouts = 0
    N = 226
    for n in range(1, 227):
        encoding = "euc-kr" if n in euc_kr else "utf-8"
        result = None
        try:
            council_url = data[n - 1]["URL"]
            council_args = args[n] if n in args.keys() else None

            if n in special_functions:
                function_name = f"scrap_{n}"
                if hasattr(sys.modules[__name__], function_name):
                    function_to_call = getattr(sys.modules[__name__], function_name)
                    if n < 57:
                        result = str(function_to_call(council_url).councilors)
                    else:
                        result = str(
                            function_to_call(council_url, args=council_args).councilors
                        )
            else:
                result = str(
                    scrap_basic(council_url, n, council_args, encoding).councilors
                )
            if "정보 없음" in result:
                print("정보 없음이 포함되어 있습니다.")
                parse_error_times += 1
            print(f"| {n} | {result}")
        except Timeout:
            print(f"| {n} | 오류: Request to {council_url} timed out.")
            timeouts += 1
        except Exception as e:
            print(f"| {n} | 오류: {e}")
            error_times += 1
            continue  # 에러가 발생하면 다음 반복으로 넘어감
    print(
        f"| 총 실행 횟수: {N} | 에러 횟수: {error_times} | 정보 없음 횟수: {parse_error_times} | 타임아웃 횟수: {timeouts} |"
    )


if __name__ == "__main__":
    main()
