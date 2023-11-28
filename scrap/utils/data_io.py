import os
import json
from dataclasses import asdict
from typing import Dict

from scrap.utils.types import ScrapResult
from db.types import Councilor


def export_results_to_json(
    results: Dict[int | str, ScrapResult], output_path: str, current_time: str
):
    os.makedirs(output_path, exist_ok=True)
    results = {
        k: [asdict(councilor) for councilor in v.councilors] for k, v in results.items()
    }

    with open(
        os.path.join(output_path, f"scraping_result_{current_time}.json"),
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(results, f, ensure_ascii=False, indent=4)


def export_results_to_txt(
    results: Dict[int | str, ScrapResult], output_path: str, current_time: str
):
    os.makedirs(output_path, exist_ok=True)
    results = {
        k: [asdict(councilor) for councilor in v.councilors] for k, v in results.items()
    }

    with open(
        os.path.join(output_path, f"scraping_result_{current_time}.txt"),
        "w",
        encoding="utf-8",
    ) as f:
        for cid, councilors in results.items():
            councilors = "\n".join([c.to_txt() for c in councilors])
            f.write(f"| {cid} | {councilors}\n")


def import_results_from_json(input_path: str, council_type: str) -> Dict[str, ScrapResult]:
    with open(input_path, "r", encoding="utf-8") as f:
        results = json.load(f)

    results = {
        k: ScrapResult(
            council_id=k,
            council_type=council_type,
            councilors=[Councilor(**c) for c in v],
        )
        for k, v in results.items()
    }

    return results