import os
import requests
import pandas as pd
from typing import List, Optional, Dict

from . import BASE_DIR, SG_TYPECODE, SG_TYPECODE_TYPE
from configurations.secrets import MongoDBSecrets
from db.client import client
from API.MongoDB import Councilor


def save_to_excel(data: List[dict], sgTypecode: str, is_elected: bool) -> None:
    directory_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    excel_file = f"[{'당선' if is_elected else '후보'}][{SG_TYPECODE[sgTypecode]}].xlsx"
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(directory_path, excel_file), index=False)

    print(f"데이터를 성공적으로 '{excel_file}'에 저장하였습니다.")


def get_local_district_id(sd_name: str, wiw_name: str) -> Optional[int]:
    db = client["district"]
    if "시" in wiw_name and "구" in wiw_name:
        wiw_name = wiw_name[: wiw_name.find("시") + 1]  # 포항시북구 -> 포항시

    district_doc = db["local_district"].find_one(
        {"sdName": sd_name, "wiwName": wiw_name}
    )
    return district_doc["cid"] if district_doc else None


def save_to_mongo(data: List[dict], sgTypecode: str) -> None:
    db = client["council"]
    main_collection = db["local_councilor"]

    local_metro_map = getLocalMetroMap()

    # TODO: Support other types of councils
    if sgTypecode == "6":
        for entry in data:
            if not (entry["sdName"], entry["wiwName"]) in local_metro_map:
                print(
                    f"Warning: '{entry['sdName']} {entry['wiwName']}'에 해당하는 지역 ID가 존재하지 않습니다."
                )
                continue
            district_id = local_metro_map[(entry["sdName"], entry["wiwName"])]
            if district_id:
                main_collection.update_one(
                    {
                        "name": entry["name"],
                        "local_id": district_id["local_id"],
                        "metro_id": district_id["metro_id"],
                    },
                    {"$set": Councilor.from_dict(entry).to_dict()},
                    upsert=True,
                )
            else:
                print(
                    f"Warning: '{entry['sdName']} {entry['wiwName']}'에 해당하는 지역 ID가 존재하지 않습니다."
                )
    else:
        raise NotImplementedError("현재 구시군의회의원(6)만 구현되어 있습니다.")

    print(f"데이터를 성공적으로 MongoDB '{main_collection.name}' 컬렉션에 저장하였습니다.")


def getLocalMetroMap() -> Dict[str, str]:
    db = client["district"]
    result = db["local_district"].aggregate(
        [
            {
                "$lookup": {
                    "from": "metro_district",
                    "localField": "sdName",
                    "foreignField": "name_ko",
                    "as": "productInfo",
                }
            },
            {"$unwind": "$productInfo"},
            {
                "$project": {
                    "cid": 1,
                    "metro_id": "$productInfo.metro_id",
                    "sdName": 1,
                    "wiwName": 1,
                }
            },
        ]
    )
    return {
        (item["sdName"], item["wiwName"]): {
            "local_id": item["cid"],
            "metro_id": item["metro_id"],
        }
        for item in result
    }
