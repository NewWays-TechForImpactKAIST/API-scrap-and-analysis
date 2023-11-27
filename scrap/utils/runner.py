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
from abc import *

from configurations.secrets import WebhookSecrets

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
from scrap.national_council import *
from scrap.group_head import *
from requests import post
from requests.exceptions import Timeout


BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)


class BaseScraper(metaclass=ABCMeta):
    def __init__(self, kwargs: Dict[str, str] = {}):
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

    def handle_errors(self, cid: int | str, error):
        self.error_log[cid] = str(error)

        if isinstance(error, Timeout):
            self.timeout_count += 1
        elif isinstance(error, ValueError) and "정보 없음" in str(error):
            self.parseerror_count += 1
        logging.error(f"| {cid} | 오류: {error}")

    def send_webhook(self, message: str) -> None:
        webhook_url = WebhookSecrets.webhook_url
        payload = {"text": message}

        response = requests.post(webhook_url, json=payload)
        if response.status_code != 200:
            raise ValueError(
                f"Request to slack returned an error {response.status_code}, the response is:\n{response.text}"
            )

    @abstractmethod
    def run(self) -> Dict[str, ScrapResult]:
        pass


class LocalCouncilScraper(BaseScraper):
    def __init__(self, kwargs: Dict[str, str] = {}):
        super().__init__(kwargs)

        runner_args_path = kwargs.get("runner_args_path")
        council_args_path = kwargs.get("council_args_path")
        data_source = kwargs.get("data_source")

        with open(runner_args_path, "r") as f:
            self.runner_args = json.load(f)
        with open(council_args_path, "r") as f:
            self.council_args = json.load(f)
        self.get_records_from_data_source(data_source)

    def get_records_from_data_source(self, data_source: str):
        if data_source == "google_sheets":
            self.url_records = read_record_from_spreadsheet()
        elif data_source == "mongodb":
            raise NotImplementedError("MongoDB에 아직 데이터가 없습니다.")

    # Helper Functions
    def is_euc_kr(self, n: int) -> bool:
        return n in self.runner_args["euc_kr"]
    def inner_euckr(self, n: int) -> bool:
        return n in self.runner_args["inner_euckr"]
    def is_special_function(self, n: int) -> bool:
        return n in self.runner_args["special_functions"]

    def is_selenium_basic(self, n: int) -> bool:
        return n in self.runner_args["selenium_basic"]

    def run_single(self, cid: int) -> ScrapResult:
        encoding = "euc-kr" if self.is_euc_kr(cid) else "utf-8"
        inner_euckr = self.inner_euckr(cid)
        council_url = self.url_records[cid - 1]["URL"]
        council_args = self.council_args.get(str(cid), None)
        if council_args is not None:
            council_args = ScrapBasicArgument(**council_args)

        if self.is_special_function(cid):
            function_name = f"scrap_{cid}"
            if hasattr(sys.modules[__name__], function_name):
                function_to_call = getattr(sys.modules[__name__], function_name)  # type: ignore
                result = function_to_call(council_url, cid, args=council_args)
            else:
                raise NotImplementedError(f"함수를 찾을 수 없습니다: {function_name}")
        else:
            if council_args is None:
                raise ValueError(f"{cid}번 의회에 대한 ScrapBasicArgument가 없습니다.")

            if self.is_selenium_basic(cid):
                result = sel_scrap_basic(council_url, cid, council_args)
            else:
                result = scrap_basic(council_url, cid, council_args, encoding, inner_euckr)

        return result

    def run(self, cids: Iterable[int], enable_webhook: bool) -> Dict[int, ScrapResult]:
        scrape_results = dict()

        for cid in tqdm(cids):
            try:
                result = self.run_single(cid)
                if "정보 없음" in str(result.councilors):
                    raise ValueError("정보 없음이 포함되어 있습니다.")
                scrape_results[cid] = result
            except Exception as e:
                self.handle_errors(cid, e)

        result_summary = f"| 총 실행 횟수: {len(cids)} | 에러: {list(self.error_log.keys())}, 총 {len(self.error_log)}회 | 그 중 정보 없음 횟수: {self.parseerror_count} | 타임아웃 횟수: {self.timeout_count} |"
        logging.info(result_summary)
        if enable_webhook:
            self.send_webhook("지방의회 스크랩 결과\n" + result_summary)

        return scrape_results


class MetroCouncilScraper(BaseScraper):
    def __init__(self, kwargs: Dict[str, str] = {}):
        super().__init__(kwargs)

    def run_single(self, cid: int) -> ScrapResult:
        function_name = f"scrap_metro_{cid}"
        if hasattr(sys.modules[__name__], function_name):
            function_to_call = getattr(sys.modules[__name__], function_name)
            result = function_to_call(cid)
        else:
            raise NotImplementedError(f"함수를 찾을 수 없습니다: {function_name}")
        return result

    def run(self, cids: Iterable[int], enable_webhook: bool) -> Dict[int, ScrapResult]:
        scrape_results = dict()

        for cid in tqdm(cids):
            try:
                result = self.run_single(cid)
                if "정보 없음" in str(result.councilors):
                    raise ValueError("정보 없음이 포함되어 있습니다.")
                scrape_results[cid] = result
            except Exception as e:
                self.handle_errors(cid, e)

        result_summary = f"| 총 실행 횟수: {len(cids)} | 에러: {list(self.error_log.keys())}, 총 {len(self.error_log)}회 | 그 중 정보 없음 횟수: {self.parseerror_count} | 타임아웃 횟수: {self.timeout_count} |"
        logging.info(result_summary)
        if enable_webhook:
            self.send_webhook("광역의회 스크랩 결과\n" + result_summary)

        return scrape_results


class NationalCouncilScraper(BaseScraper):
    def __init__(self, kwargs: Dict[str, str] = {}):
        super().__init__(kwargs)

    def run(self) -> Dict[str, ScrapResult]:
        result = dict()

        try:
            result["국회"] = scrap_national_council()
        except Exception as e:
            self.handle_errors("국회", e)

        return result


class LeadersScraper(BaseScraper):
    def __init__(self, kwargs: Dict[str, str] = {}):
        super().__init__(kwargs)

    def run(self) -> Dict[str, ScrapResult]:
        result = dict()

        try:
            results = scrap_group_leaders()
        except Exception as e:
            self.handle_errors("단체장", e)

        return results


class ScraperFactory:
    def __init__(self, where: str, kwargs: Dict[str, str] = {}):
        self.where = where
        self.kwargs = kwargs

    def create_scraper(self) -> BaseScraper:
        if self.where == "local":
            return LocalCouncilScraper(self.kwargs)
        elif self.where == "metro":
            return MetroCouncilScraper(self.kwargs)
        elif self.where == "leaders":
            return LeadersScraper(self.kwargs)
        elif self.where == "national":
            return NationalCouncilScraper(self.kwargs)
        else:
            raise ValueError(f"알 수 없는 의회: {self.where}")


def main(args: Dict[str, str]) -> None:
    warnings.filterwarnings("ignore")

    where = args.get("where")
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    runner_kwargs = args | {"current_time": current_time}

    runner = ScraperFactory(where, runner_kwargs).create_scraper()

    cids_to_run = parse_cids(args.get("cids"), where)
    enable_webhook = args.get("disable-webhook")
    if cids_to_run:
        results = runner.run(cids_to_run, enable_webhook)
    else:
        results = runner.run()

    if args.get("update-mongo"):
        for result in results.values():
            save_to_database(result)

    if args.get("output-store"):
        if args.get("output-format") == "json":
            export_results_to_json(results, args.get("output-path"), current_time)
        elif args.get("output-format") == "txt":
            export_results_to_txt(results, args.get("output-path"), current_time)


def parse_cids(cids_str: Optional[str], where: str) -> Optional[Iterable[int]]:
    if cids_str and where in ["local", "metro"]:
        return [int(cid.strip()) for cid in cids_str.split(",")]
    elif where == "metro":
        return range(1, 18)
    elif where == "local":
        return range(1, 227)
    elif where == "national":
        return None
    elif where == "leaders":
        return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="지방의회 / 광역의회 / 국회 / 단체장 스크랩 스크립트 실행")
    parser.add_argument(
        "-w",
        "--where",
        help="스크랩할 의회 종류 (지방의회: 'local', 광역의회: 'metro', 국회: 'national', 단체장: 'leaders')",
        choices=["local", "metro", "national", "leaders"],
        default="local",
    )
    parser.add_argument(
        "--data-source",
        help="사용할 데이터 소스 ('google_sheets', 'mongodb')",
        choices=["google_sheets", "mongodb"],
        default="google_sheets",
    )
    parser.add_argument("-l", "--log_path", help="로그 파일 경로", default="logs")
    parser.add_argument(
        "-m", "--update-mongo", help="스크랩 결과를 MongoDB에 업데이트", action="store_true"
    )
    parser.add_argument(
        "-o", "--output-store", help="스크랩 결과를 로컬에 저장", action="store_true"
    )
    parser.add_argument(
        "--output-format",
        help="스크랩 결과 저장 형식 ('json', 'txt')",
        choices=["json", "txt"],
        default="json",
    )
    parser.add_argument("--output-path", help="스크랩 결과 저장 경로", default="output")
    parser.add_argument(
        "-c", "--cids", help="스크랩할 의회 ID 목록 (','로 구분, 지방/광역의회만 해당)", default=None
    )
    parser.add_argument(
        "--runner-args-path",
        help="지방의회 스크랩 시 사용할 runner_args JSON 파일 경로",
        default="scrap/utils/runner_args.json",
    )
    parser.add_argument(
        "--council-args-path",
        help="지방의회 스크랩 시 사용할 council_args JSON 파일 경로",
        default="scrap/utils/scrap_args.json",
    )
    parser.add_argument(
        "--disable-webhook",
        help="스크랩 결과 웹훅 전송 비활성화",
        action="store_false",
    )
    args = vars(parser.parse_args())

    main(args)
