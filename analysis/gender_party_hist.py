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


# ===================================
#     Gender history calculations
# ===================================


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

    df["wiwName"] = df["wiwName"].apply(lambda x: x if isinstance(x, str) else "")
    df["sdName"] = df[["sdName", "wiwName"]].apply(
        lambda x: local_to_metro_list(*x), axis=1
    )
    df["wiwName"] = df[["sdName", "wiwName"]].apply(
        lambda x: change_local_name(*x), axis=1
    )
    df["sdName"] = df[["sdName", "wiwName"]].apply(
        lambda x: "대구광역시" if x[1] == "군위군" else x[0], axis=1
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


# ===================================
#     Party history calculations
# ===================================


def party_hist(councilor_type: str, level: int, is_elected: bool, filenames: list[str]):
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
    party_hist_collection = client["stats"].get_collection("party_hist")

    df["wiwName"] = df["wiwName"].apply(lambda x: x if isinstance(x, str) else "")
    df["sdName"] = df[["sdName", "wiwName"]].apply(
        lambda x: local_to_metro_list(*x), axis=1
    )
    df["wiwName"] = df[["sdName", "wiwName"]].apply(
        lambda x: change_local_name(*x), axis=1
    )
    df["sdName"] = df[["sdName", "wiwName"]].apply(
        lambda x: "대구광역시" if x[1] == "군위군" else x[0], axis=1
    )

    if level == 0:
        df = df[["sgId", "name", "jdName"]].groupby(by=["sgId", "jdName"]).count()
        for idx in df.index:
            year = int(str(idx[0])[:4])
            print(f"{year=}")
            party_hist_collection.find_one_and_update(
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
            df[["sgId", "sdName", "name", "jdName"]]
            .groupby(by=["sgId", "sdName", "jdName"])
            .count()
        )
        for idx in df.index:
            year = int(str(idx[0])[:4])
            print(f"{year=} sdName={idx[1]}")
            metroId = district_db.get_collection("metro_district").find_one(
                {"sdName": idx[1]}
            )["metroId"]

            party_hist_collection.find_one_and_update(
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
            df[["sgId", "sdName", "wiwName", "name", "jdName"]]
            .groupby(by=["sgId", "sdName", "wiwName", "jdName"])
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

            party_hist_collection.find_one_and_update(
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


# ===================================================
#  Age history calculations for national councilors
# ===================================================


def age_hist_national(is_elected: bool, filenames: list[str]):
    datadir = os.path.join(BASE_DIR, "_data")
    df = pd.DataFrame()

    for d in filenames:
        df_new = pd.read_excel(os.path.join(datadir, d))
        df = pd.concat([df, df_new])

    df = df[["sgId", "name", "age"]].groupby(by=["sgId", "age"]).count().reset_index()
    df["cumsum"] = df.groupby(by="sgId")["name"].cumsum()
    df["quintile"] = pd.qcut(df["cumsum"], q=5, labels=[0, 1, 2, 3, 4])

    total = (
        df[["sgId", "name"]]
        .groupby(by=["sgId"])
        .sum()
        .rename(columns={"name": "total"})
    )
    first_quintile = (
        df.loc[df["quintile"] == 0]
        .groupby(by=["sgId"])
        .max()[["age"]]
        .rename(columns={"age": "q1"})
    )
    last_quintile = (
        df.loc[df["quintile"] == 4]
        .groupby(by=["sgId"])
        .min()[["age"]]
        .rename(columns={"age": "q5"})
    )
    quintiles = pd.concat([total, first_quintile, last_quintile], axis=1)

    hist_data: dict[int, list[dict]] = {}
    for _, row in df.iterrows():
        year = int(str(row["sgId"])[:4])
        age = int(row["age"])
        cnt = int(row["name"])
        age_group = int(row["quintile"])

        if year in hist_data:
            hist_data[year].append(
                {"minAge": age, "maxAge": age + 1, "count": cnt, "ageGroup": age_group}
            )
        else:
            hist_data[year] = [
                {"minAge": age, "maxAge": age + 1, "count": cnt, "ageGroup": age_group}
            ]

    stat_data: dict[int, dict] = {}
    for sgId, row in quintiles.iterrows():
        year = int(str(sgId)[:4])
        stat_data[year] = {
            "firstquintile": int(row["q1"]),
            "lastquintile": int(row["q5"]),
            "population": int(row["total"]),
        }

    age_hist_collection = client["stats"].get_collection("age_hist")
    for year, docs in hist_data.items():
        age_hist_collection.find_one_and_update(
            {
                "councilorType": "national_councilor",
                "is_elected": is_elected,
                "level": 0,
                "method": "equal",
                "year": year,
            },
            {"$set": {"data": docs}},
            upsert=True,
        )

    age_stat_collection = client["stats"].get_collection("age_stat")
    for year, doc in stat_data.items():
        age_stat_collection.find_one_and_update(
            {
                "councilorType": "national_councilor",
                "is_elected": is_elected,
                "level": 0,
                "method": "equal",
                "year": year,
            },
            {"$set": {"data": [doc]}},
            upsert=True,
        )


def main():
    gender_hist(
        "local_councilor", 2, True, ["[당선][구시군의회의원].xlsx", "[당선][기초의원비례대표].xlsx"]
    )
    gender_hist(
        "local_councilor", 2, False, ["[후보][구시군의회의원].xlsx", "[후보][기초의원비례대표].xlsx"]
    )

    gender_hist("metro_councilor", 1, True, ["[당선][시도의원].xlsx", "[당선][광역의원비례대표].xlsx"])
    gender_hist("metro_councilor", 1, False, ["[후보][시도의원].xlsx", "[후보][광역의원비례대표].xlsx"])

    gender_hist("national_councilor", 0, True, ["[당선][국회의원].xlsx"])
    gender_hist("national_councilor", 0, False, ["[후보][국회의원].xlsx"])

    gender_hist_add_zero()

    party_hist(
        "local_councilor", 2, True, ["[당선][구시군의회의원].xlsx", "[당선][기초의원비례대표].xlsx"]
    )
    party_hist(
        "local_councilor", 2, False, ["[후보][구시군의회의원].xlsx", "[후보][기초의원비례대표].xlsx"]
    )

    party_hist("metro_councilor", 1, True, ["[당선][시도의원].xlsx", "[당선][광역의원비례대표].xlsx"])
    party_hist("metro_councilor", 1, False, ["[후보][시도의원].xlsx", "[후보][광역의원비례대표].xlsx"])

    party_hist("national_councilor", 0, True, ["[당선][국회의원].xlsx"])
    party_hist("national_councilor", 0, False, ["[후보][국회의원].xlsx"])

    age_hist_national(True, ["[당선][국회의원].xlsx"])
    age_hist_national(False, ["[후보][국회의원].xlsx"])


if __name__ == "__main__":
    main()
