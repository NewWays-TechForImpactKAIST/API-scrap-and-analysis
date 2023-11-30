# coding=utf-8
import pandas as pd
import os
import warnings
from db.client import client
from analysis.age.hist_groups import (
    local_to_metro_list,
    change_local_name,
    cluster_data,
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
    age_hist_collection = client["stats"].get_collection("age_hist")
    age_stat_collection = client["stats"].get_collection("age_stat")
    # paramter
    method = "equal"
    n_clst = 5

    datadir = os.path.join(BASE_DIR, "_data")
    df_original = pd.DataFrame()

    for d in filenames:
        df_new = pd.read_excel(os.path.join(datadir, d))
        df_original = pd.concat([df_original, df_new])
    # df_original = df_original[["sgId", "name", "age"]].groupby(by=["sgId", "age"]).count().reset_index()
    df_original["year"] = df_original["sgId"] // 10000
    df_original = df_original[df_original["year"].isin([2008, 2012, 2016, 2020, 2024])]
    years = df_original["year"].unique()
    for year in years:
        year = int(year)
        df = df_original[df_original["year"] == year]
        df = cluster_data(method, n_clst, df)
        first_q = df[df["cluster_label"] == 0]["age"].max()
        last_q = df[df["cluster_label"] == n_clst - 1]["age"].min()
        # 히스토그램을 그립니다.
        histdata = [
            {
                "minAge": int(age),
                "maxAge": int(age) + 1,
                "count": df[df["age"] == age].shape[0],
                "ageGroup": int(df.loc[df["age"] == age].iloc[0]["cluster_label"]),
            }
            for age in df["age"].unique()
        ]
        statdata = None
        if method == "equal":
            statdata = [
                {
                    "firstquintile": int(first_q),
                    "lastquintile": int(last_q),
                    "population": int(df.shape[0]),
                }
            ]
        age_hist_collection.find_one_and_update(
            {
                "councilorType": "national_councilor",
                "is_elected": is_elected,
                "level": 0,
                "method": "equal",
                "year": year,
            },
            {"$set": {"data": histdata}},
            upsert=True,
        )
        if method == "equal":
            age_stat_collection.find_one_and_update(
                {
                    "councilorType": "national_councilor",
                    "is_elected": is_elected,
                    "level": 0,
                    "method": "equal",
                    "year": year,
                },
                {"$set": {"data": statdata}},
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
