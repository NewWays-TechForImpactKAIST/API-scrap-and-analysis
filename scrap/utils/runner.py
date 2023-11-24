import os
import sys
import json
import argparse
import datetime
import logging
import warnings
from typing import List, Dict, Optional
from collections.abc import Iterable
from tqdm import tqdm

from scrap.utils.export import export_results_to_json, export_results_to_txt
from scrap.utils.database import save_to_database
from scrap.utils.types import ScrapResult, ScrapBasicArgument
from scrap.utils.spreadsheet import read_record_from_spreadsheet
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
from scrap.metropolitan_council import *
from requests.exceptions import Timeout


BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)


class ScraperRunner:
    def __init__(
        self,
        runner_args_path: str,
        council_args_path: str,
        data_source: str,
        kwargs: Dict[str, str] = {},
    ):
        if runner_args_path is None or council_args_path is None or data_source is None:
            pass
        else:
            with open(runner_args_path, "r") as f:
                self.runner_args = json.load(f)
            with open(council_args_path, "r") as f:
                self.council_args = json.load(f)

            self.get_records_from_data_source(data_source)

        self.setup_logging(kwargs.get("log_path"), kwargs.get("current_time"))
        self.error_log = dict()
        self.timeout_count = 0
        self.parseerror_count = 0

    def setup_logging(self, log_path: str, current_time: str):
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        log_path = os.path.join(BASE_DIR, log_path, f"scraping_log_{current_time}.log")

        logging.basicConfig(
            filename=log_path,
            level=logging.INFO,
            format="[%(asctime)s] %(levelname)s - %(message)s",
        )

    def get_records_from_data_source(self, data_source: str):
        if data_source == "google_sheets":
            self.url_records = read_record_from_spreadsheet()
        elif data_source == "mongodb":
            # TODO: Implement MongoDB -> MongoDB에 지방의회별 URL을 저장할 필요성 논의
            raise NotImplementedError("MongoDB에 아직 데이터가 없습니다.")

    # Helper Functions
    def is_euc_kr(self, n: int) -> bool:
        return n in self.runner_args["euc_kr"]

    def is_special_function(self, n: int) -> bool:
        return n in self.runner_args["special_functions"]

    def is_selenium_basic(self, n: int) -> bool:
        return n in self.runner_args["selenium_basic"]

    def handle_errors(self, cid: int, error):
        self.error_log[cid] = str(error)

        if isinstance(error, Timeout):
            self.timeout_count += 1
        elif isinstance(error, ValueError) and "정보 없음" in str(error):
            self.parseerror_count += 1
        logging.error(f"| {cid} | 오류: {error}")

    def run_single_council(self, n: int) -> ScrapResult:
        encoding = "euc-kr" if self.is_euc_kr(n) else "utf-8"
        council_url = self.url_records[n - 1]["URL"]
        council_args = self.council_args.get(str(n), None)
        if council_args is not None:
            council_args = ScrapBasicArgument(**council_args)

        if self.is_special_function(n):
            function_name = f"scrap_{n}"
            if hasattr(sys.modules[__name__], function_name):
                function_to_call = getattr(sys.modules[__name__], function_name)  # type: ignore
                result = function_to_call(council_url, n, args=council_args)
            else:
                raise NotImplementedError(f"함수를 찾을 수 없습니다: {function_name}")
        else:
            if council_args is None:
                raise ValueError(f"{n}번 의회에 대한 ScrapBasicArgument가 없습니다.")

            if self.is_selenium_basic(n):
                result = sel_scrap_basic(council_url, n, council_args)
            else:
                result = scrap_basic(council_url, n, council_args, encoding)

        return result

    def run_single_metro(self, n: int) -> ScrapResult:
        function_name = f"scrap_metro_{n}"
        if hasattr(sys.modules[__name__], function_name):
            function_to_call = getattr(sys.modules[__name__], function_name)
            result = function_to_call(n)
        else:
            raise NotImplementedError(f"함수를 찾을 수 없습니다: {function_name}")
        return result

    def run_heads(self) -> ScrapResult:
        raise NotImplementedError("단체장 스크랩")

    def run_nationals(self) -> ScrapResult:
        raise NotImplementedError("국회 스크랩")

    def run_all_councils(self, cids: Iterable[int]) -> Dict[int, ScrapResult]:
        scrape_results = dict()

        for cid in tqdm(cids):
            try:
                result = self.run_single_council(cid)
                if "정보 없음" in str(result.councilors):
                    raise ValueError("정보 없음이 포함되어 있습니다.")
                scrape_results[cid] = result
            except Exception as e:
                self.handle_errors(cid, e)

    def run_all_metros(self, cids: Iterable[int]) -> Dict[int, ScrapResult]:
        scrape_results = dict()

        for cid in tqdm(cids):
            try:
                result = self.run_single_metro(cid)
                if "정보 없음" in str(result.councilors):
                    raise ValueError("정보 없음이 포함되어 있습니다.")
                scrape_results[cid] = result
            except Exception as e:
                self.handle_errors(cid, e)

        logging.info(
            f"| 총 실행 횟수: {len(cids)} | 에러: {list(self.error_log.keys())}, 총 {len(self.error_log)}회 | 그 중 정보 없음 횟수: {self.parseerror_count} | 타임아웃 횟수: {self.timeout_count} |"
        )

        return scrape_results


def main(args: Dict[str, str]) -> None:
    warnings.filterwarnings("ignore")

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    runner_kwargs = {
        "log_path": args.get("log_path"),
        "current_time": current_time,
    }
    where = "local_council"
    if args.get("where") == "1":
        where = "metro_council"
    elif args.get("where") == "3":
        where = "heads"
    elif args.get("where") == "4":
        where = "national_council"
    if where == "local_council":
        runner = ScraperRunner(
            args["runner_args_path"],
            args["council_args_path"],
            args["data_source"],
            runner_kwargs,
        )
    else:
        runner = ScraperRunner(
            None,
            None,
            None,
            runner_kwargs,
        )

    cids_to_run = parse_cids(args.get("cids"), where)
    if where == "local_council":
        results = runner.run_all_councils(cids_to_run)
    elif where == "metro_council":
        results = runner.run_all_metros(cids_to_run)
    elif where == "heads":
        results = runner.run_heads()
    else:
        assert where == "national_council"
        results = runner.run_nationals()

    if args.get("update_mongo"):
        for result in results.values():
            # TODO: 잘 작동하는지 확인 필요
            save_to_database(result)

    if args.get("output_store"):
        if args.get("output_format") == "json":
            export_results_to_json(results, args.get("output_path"), current_time)
        elif args.get("output_format") == "txt":
            export_results_to_txt(results, args.get("output_path"), current_time)


def parse_cids(cids_str: Optional[str], where: str) -> list[int]:
    if cids_str:
        return [int(cid.strip()) for cid in cids_str.split(",")]
    elif where == "metro_council":
        return range(1, 18)
    elif where == "local_council":
        return range(1, 227)
    elif where == "heads":
        raise NotImplementedError("단체장 스크랩은 몇부터 몇까지죠?")
    elif where == "national_council":
        raise NotImplementedError("국회 스크랩은 몇부터 몇까지죠?")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="지방의회/광역의회/국회/단체장\
                                     스크랩 스크립트 실행"
    )
    parser.add_argument(
        "data_source",
        help="사용할 데이터 소스 ('google_sheets', 'mongodb')",
        choices=["google_sheets", "mongodb"],
        default="google_sheets",
    )
    parser.add_argument("-w", "--where", help="1 = 광역의회, 2 = 지방의회, 3 = 단체장, 4 = 국회")
    parser.add_argument("-c", "--cids", help="스크랩할 지방의회 ID 목록 (쉼표로 구분)", default=None)
    parser.add_argument("-l", "--log_path", help="로그 파일 경로", default="logs")
    parser.add_argument(
        "-m", "--update_mongo", help="스크랩 결과를 MongoDB에 업데이트", action="store_true"
    )
    parser.add_argument(
        "-o", "--output_store", help="스크랩 결과를 로컬에 저장", action="store_true"
    )
    parser.add_argument(
        "--output_format",
        help="스크랩 결과 저장 형식 ('json', 'txt')",
        choices=["json", "txt"],
        default="json",
    )
    parser.add_argument("--output_path", help="스크랩 결과 저장 경로", default="output")
    parser.add_argument(
        "-rpath",
        "--runner_args_path",
        help="runner_args JSON 파일 경로",
        default="scrap/utils/runner_args.json",
    )
    parser.add_argument(
        "-cpath",
        "--council_args_path",
        help="council_args JSON 파일 경로",
        default="scrap/utils/council_args.json",
    )
    args = vars(parser.parse_args())

    main(args)
