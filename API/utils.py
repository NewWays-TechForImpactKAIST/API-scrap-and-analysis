import os
import requests
import pandas as pd
from typing import List, Optional, Dict

from . import BASE_DIR, SG_TYPECODE
from configurations.secrets import MongoDBSecrets
from db.client import client
from API.MongoDB import Councilor


LOCAL_METRO_ID_MAP = None


def save_to_excel(data: List[dict], sgTypecode: str, is_elected: bool) -> None:
    directory_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    excel_file = f"[{'당선' if is_elected else '후보'}][{SG_TYPECODE[sgTypecode]}].xlsx"
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(directory_path, excel_file), index=False)

    print(f"데이터를 성공적으로 '{excel_file}'에 저장하였습니다.")


def get_district_id(sd_name: str, wiw_name: str) -> Optional[int]:
    global LOCAL_METRO_ID_MAP
    if not LOCAL_METRO_ID_MAP:
        LOCAL_METRO_ID_MAP = getLocalMetroMap()

    if "시" in wiw_name and "구" in wiw_name:
        wiw_name = wiw_name[: wiw_name.find("시") + 1]  # 포항시북구 -> 포항시

    if (sd_name, wiw_name) not in LOCAL_METRO_ID_MAP.keys():
        return None
    return LOCAL_METRO_ID_MAP[(sd_name, wiw_name)]


def save_to_mongo(data: List[dict], sgTypecode: str, where: str) -> None:
    db = client["council"]
    main_collection = db[where]

    # TODO: Support other types of councils
    if sgTypecode in ["6", "9"]:
        for entry in data:
            district_id = get_district_id(entry["sdName"], entry["wiwName"])

            if district_id:
                main_collection.update_one(
                    {
                        "name": entry["name"],
                        "localId": district_id["localId"],
                        "metroId": district_id["metroId"],
                    },
                    {"$set": Councilor.from_dict(entry).to_dict()},
                    upsert=True,
                )
            else:
                print(
                    f"Warning: '{entry['sdName']} {entry['wiwName']}'에 해당하는 지역 ID가 존재하지 않습니다."
                )
    else:
        raise NotImplementedError("현재 구시군의회의원(6) 및 기초의원비례대표(9)만 구현되어 있습니다.")

    print(f"데이터를 성공적으로 MongoDB '{main_collection.name}' 컬렉션에 저장하였습니다.")


def getLocalMetroMap() -> Dict[str, str]:
    db = client["district"]
    result = db["local_district"].aggregate(
        [
            {
                "$lookup": {
                    "from": "metro_district",
                    "localField": "sdName",
                    "foreignField": "sdName",
                    "as": "productInfo",
                }
            },
            {"$unwind": "$productInfo"},
            {
                "$project": {
                    "localId": 1,
                    "metroId": "$productInfo.metroId",
                    "sdName": 1,
                    "wiwName": 1,
                }
            },
        ]
    )
    return {
        (item["sdName"], item["wiwName"]): {
            "localId": item["localId"],
            "metroId": item["metroId"],
        }
        for item in result
    }
