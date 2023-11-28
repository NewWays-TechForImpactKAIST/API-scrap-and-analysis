# coding=utf-8
import pandas as pd
import os
import warnings
from db.client import client
from analysis.age.hist_groups import (
    local_to_metro_list,
    change_local_name,
)

# 경고 무시
warnings.filterwarnings("ignore", category=FutureWarning)

BASE_DIR = os.path.join(os.path.dirname(__file__), os.pardir)


councilordict = {
    "시도의원": "metro_councilor",
    "광역의원비례대표": "metro_councilor",
    "구시군의회의원": "local_councilor",
    "기초의원비례대표": "local_councilor",
}


def gender_hist(
    councilor_type: str, level: int, is_elected: bool, filenames: list[str]
):
    ## TO-DO: excel말고 mongodb에서 받아오도록 합니다.
    assert (councilor_type, level) in [
        ("local_councilor", 2),
        ("metro_councilor", 1),
        ("national_councilor", 0),
    ]
    datadir = os.path.join(BASE_DIR, "_data")
    df = pd.DataFrame()

    for d in filenames:
        df_new = pd.read_excel(os.path.join(datadir, d))
        df = pd.concat([df, df_new])

    district_db = client["district"]
    gender_hist_collection = client["stats"].get_collection("gender_hist")

    df["sdName"] = df[["sdName", "wiwName"]].apply(
        lambda x: local_to_metro_list(*x), axis=1
    )
    df["wiwName"] = df[["sdName", "wiwName"]].apply(
        lambda x: change_local_name(*x), axis=1
    )

    if level == 0:
        df = df[["sgId", "name", "gender"]].groupby(by=["sgId", "gender"]).count()
        for idx in df.index:
            year = int(str(idx[0])[:4])
            print(f"{year=}")
            gender_hist_collection.find_one_and_update(
                {
                    "councilorType": "national_councilor",
                    "is_elected": is_elected,
                    "level": 0,
                    "year": year,
                },
                {"$set": {idx[1]: int(df["name"][idx])}},
                upsert=True,
            )

    elif level == 1:
        df = (
            df[["sgId", "sdName", "name", "gender"]]
            .groupby(by=["sgId", "sdName", "gender"])
            .count()
        )
        for idx in df.index:
            year = int(str(idx[0])[:4])
            print(f"{year=} sdName={idx[1]}")
            metroId = district_db.get_collection("metro_district").find_one(
                {"sdName": idx[1]}
            )["metroId"]

            gender_hist_collection.find_one_and_update(
                {
                    "councilorType": "metro_councilor",
                    "is_elected": is_elected,
                    "level": 1,
                    "metroId": metroId,
                    "year": year,
                },
                {"$set": {idx[2]: int(df["name"][idx])}},
                upsert=True,
            )

    elif level == 2:
        df = (
            df[["sgId", "sdName", "wiwName", "name", "gender"]]
            .groupby(by=["sgId", "sdName", "wiwName", "gender"])
            .count()
        )
        for idx in df.index:
            year = int(str(idx[0])[:4])
            print(f"{year=} sdName={idx[1]} wiwName={idx[2]}")
            doc = district_db["local_district"].find_one(
                {
                    "sdName": idx[1],
                    "wiwName": idx[2] if idx[1] != "세종특별자치시" else "세종특별자치시",
                }
            )
            metroId, localId = doc["metroId"], doc["localId"]

            gender_hist_collection.find_one_and_update(
                {
                    "councilorType": "local_councilor",
                    "is_elected": is_elected,
                    "level": 2,
                    "metroId": metroId,
                    "localId": localId,
                    "year": year,
                },
                {"$set": {idx[3]: int(df["name"][idx])}},
                upsert=True,
            )


def gender_hist_add_zero():
    gender_hist_collection = client["stats"].get_collection("gender_hist")
    gender_hist_collection.update_many({"남": {"$exists": False}}, {"$set": {"남": 0}})
    gender_hist_collection.update_many({"여": {"$exists": False}}, {"$set": {"여": 0}})


def main():
    gender_hist("local_councilor", 2, True, ["[당선][구시군의회의원].xlsx"])
    gender_hist("local_councilor", 2, False, ["[후보][구시군의회의원].xlsx"])

    gender_hist("metro_councilor", 1, True, ["[당선][시도의원].xlsx"])
    gender_hist("metro_councilor", 1, False, ["[후보][시도의원].xlsx"])

    gender_hist("national_councilor", 0, True, ["[당선][국회의원].xlsx"])
    gender_hist("national_councilor", 0, False, ["[후보][국회의원].xlsx"])

    gender_hist_add_zero()


main()
