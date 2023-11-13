import os
import requests
import pandas as pd
from typing import List

from . import BASE_DIR, SG_TYPECODE, SG_TYPECODE_TYPE
from configurations.secrets import MongoDBSecrets
from db.client import client


def save_to_excel(data: List[dict], sgTypecode: str, is_elected: bool) -> None:
    directory_path = os.path.join(BASE_DIR, "output")
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    excel_file = f"[{'당선' if is_elected else '후보'}][{SG_TYPECODE[sgTypecode]}].xlsx"
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(directory_path, excel_file), index=False)

    print(f"데이터를 성공적으로 '{excel_file}'에 저장하였습니다.")


def save_to_mongo(data: List[dict], sgTypecode: str) -> None:
    db = client[str(MongoDBSecrets.database_name)]
    collection = db[str(SG_TYPECODE_TYPE[sgTypecode])]

    # TODO: 지역구별로 분리하여 업데이트하는 로직 추가
    collection.insert_many(data)

    print(f"데이터를 MongoDB의 '{collection_name}' 컬렉션에 저장하였습니다.")
