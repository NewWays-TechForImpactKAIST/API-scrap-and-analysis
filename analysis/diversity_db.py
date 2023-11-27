from collections import Counter
import math
from pymongo.operations import UpdateOne

from db.client import client


# ====================================
#     Diversity index calculations
# ====================================


def count(data, stair=0):
    """
    Returns a counter object of the data, while stairing them to appropriate bins if stair > 0
    """
    if stair > 0:
        if isinstance(data[0], str):
            raise TypeError("stair is not defined for string data")
        data = [math.floor(d / stair) * stair for d in data]
    return Counter(data)


def gini_simpson(data, stair=0, opts=True):
    """
    Gini-Simpson diversity index
    """
    counts = count(data, stair)
    total = sum(counts.values())
    gs_idx = 1 - sum((n / total) * ((n - 1) / (total - 1)) for n in counts.values())

    if opts:
        num_cats = len([c for c in counts.values() if c > 0])
        if num_cats <= 1:
            return 0.0
        max_gs_idx = (num_cats - 1) / num_cats * total / (total - 1)
        gs_idx /= max_gs_idx

    return gs_idx


def shannon(data, stair=0, opts=True):
    """
    Shannon diversity index
    """
    counts = count(data, stair)
    total = sum(counts.values())
    sh_idx = -sum((n / total) * math.log(n / total) for n in counts.values())

    if opts:
        num_cats = len([c for c in counts.values() if c > 0])
        max_sh_idx = math.log(num_cats)
        sh_idx /= max_sh_idx

    return sh_idx


# ====================================
#  Local council diversity statistics
# ====================================


def save_to_mongo_local(localId: int, factor: str, stair=0, opts=True) -> None:
    factor_field = {"age": "age", "gender": "gender", "party": "jdName"}
    data = [
        councilor[factor_field[factor]]
        for councilor in client["council"]["local_councilor"].find({"localId": localId})
    ]
    # print(f"{localId} {factor}")
    # print(data)
    client["stats"].get_collection("diversity_index").update_one(
        {"localId": localId},
        {"$set": {f"{factor}DiversityIndex": gini_simpson(data, stair, opts)}},
        upsert=True,
    )


def calculate_rank_local(factor: str) -> None:
    result = client["stats"]["diversity_index"].aggregate(
        [
            {"$match": {"localId": {"$ne": None}}},
            {"$sort": {f"{factor}DiversityIndex": -1}},
            {"$group": {"_id": "", "items": {"$push": "$$ROOT"}}},
            {"$unwind": {"path": "$items", "includeArrayIndex": "items.rank"}},
            {"$replaceRoot": {"newRoot": "$items"}},
            {"$addFields": {"rank": {"$add": ["$rank", 1]}}},
        ]
    )
    for doc in result:
        client["stats"]["diversity_index"].find_one_and_update(
            {"localId": doc["localId"]},
            {"$set": {f"{factor}DiversityRank": int(doc["rank"])}},
        )


def calculate_age_diversity_rank_history_local() -> None:
    for is_elected in [True, False]:
        for localId in range(1, 227):
            docs = client["stats"]["age_hist"].find(
                {
                    "councilorType": "local_councilor",
                    "is_elected": is_elected,
                    "method": "equal",
                    "level": 2,
                    "localId": localId,
                }
            )
            for doc in docs:
                diversity_index = gini_simpson(
                    [
                        group["minAge"]
                        for group in doc["data"]
                        for _ in range(group["count"])
                    ],
                    stair=10,
                )
                client["stats"]["age_hist"].find_one_and_update(
                    {
                        "councilorType": "local_councilor",
                        "is_elected": is_elected,
                        "method": "equal",
                        "level": 2,
                        "localId": localId,
                        "year": doc["year"],
                    },
                    {"$set": {"diversityIndex": diversity_index}},
                )

        years = list({doc["year"] for doc in client["stats"]["age_hist"].find()})

        for year in years:
            result = client["stats"]["age_hist"].aggregate(
                [
                    {
                        "$match": {
                            "councilorType": "local_councilor",
                            "is_elected": is_elected,
                            "method": "equal",
                            "level": 2,
                            "year": year,
                        }
                    },
                    {"$sort": {"diversityIndex": -1}},
                    {"$group": {"_id": "", "items": {"$push": "$$ROOT"}}},
                    {"$unwind": {"path": "$items", "includeArrayIndex": "items.rank"}},
                    {"$replaceRoot": {"newRoot": "$items"}},
                    {"$addFields": {"rank": {"$add": ["$rank", 1]}}},
                ]
            )
            for doc in result:
                client["stats"]["age_hist"].find_one_and_update(
                    {
                        "councilorType": "local_councilor",
                        "is_elected": is_elected,
                        "method": "equal",
                        "level": 2,
                        "localId": doc["localId"],
                        "year": year,
                    },
                    {"$set": {"diversityRank": int(doc["rank"])}},
                )


# ====================================
#  Metro council diversity statistics
# ====================================


def save_to_mongo_metro(metroId: int, factor: str, stair=0, opts=True) -> None:
    factor_field = {"age": "age", "gender": "gender", "party": "jdName"}
    data = [
        councilor[factor_field[factor]]
        for councilor in client["council"]["metro_councilor"].find({"metroId": metroId})
    ]
    # print(f"{metroId} {factor}")
    # print(data)
    client["stats"].get_collection("diversity_index").update_one(
        {"metroId": metroId},
        {"$set": {f"{factor}DiversityIndex": gini_simpson(data, stair, opts)}},
        upsert=True,
    )


def calculate_rank_metro(factor: str) -> None:
    result = client["stats"]["diversity_index"].aggregate(
        [
            {"$match": {"metroId": {"$ne": None}}},
            {"$sort": {f"{factor}DiversityIndex": -1}},
            {"$group": {"_id": "", "items": {"$push": "$$ROOT"}}},
            {"$unwind": {"path": "$items", "includeArrayIndex": "items.rank"}},
            {"$replaceRoot": {"newRoot": "$items"}},
            {"$addFields": {"rank": {"$add": ["$rank", 1]}}},
        ]
    )
    for doc in result:
        client["stats"]["diversity_index"].find_one_and_update(
            {"metroId": doc["metroId"]},
            {"$set": {f"{factor}DiversityRank": int(doc["rank"])}},
        )


def calculate_age_diversity_rank_history_metro() -> None:
    for is_elected in [True, False]:
        for metroId in range(1, 18):
            docs = client["stats"]["age_hist"].find(
                {
                    "councilorType": "metro_councilor",
                    "method": "equal",
                    "level": 1,
                    "is_elected": is_elected,
                    "metroId": metroId,
                }
            )
            for doc in docs:
                diversity_index = gini_simpson(
                    [
                        group["minAge"]
                        for group in doc["data"]
                        for _ in range(group["count"])
                    ],
                    stair=10,
                )
                client["stats"]["age_hist"].find_one_and_update(
                    {
                        "councilorType": "metro_councilor",
                        "method": "equal",
                        "level": 1,
                        "is_elected": is_elected,
                        "metroId": metroId,
                        "year": doc["year"],
                    },
                    {"$set": {"diversityIndex": diversity_index}},
                )

        years = list({doc["year"] for doc in client["stats"]["age_hist"].find()})

        for year in years:
            result = client["stats"]["age_hist"].aggregate(
                [
                    {
                        "$match": {
                            "councilorType": "metro_councilor",
                            "method": "equal",
                            "level": 1,
                            "is_elected": is_elected,
                            "year": year,
                        }
                    },
                    {"$sort": {"diversityIndex": -1}},
                    {"$group": {"_id": "", "items": {"$push": "$$ROOT"}}},
                    {"$unwind": {"path": "$items", "includeArrayIndex": "items.rank"}},
                    {"$replaceRoot": {"newRoot": "$items"}},
                    {"$addFields": {"rank": {"$add": ["$rank", 1]}}},
                ]
            )
            for doc in result:
                client["stats"]["age_hist"].find_one_and_update(
                    {
                        "councilorType": "metro_councilor",
                        "method": "equal",
                        "level": 1,
                        "is_elected": is_elected,
                        "metroId": doc["metroId"],
                        "year": year,
                    },
                    {"$set": {"diversityRank": int(doc["rank"])}},
                )


# =====================================
# National council diversity statistics
# =====================================


def save_to_mongo_national(factor: str, stair=0, opts=True) -> None:
    factor_field = {"age": "age", "gender": "gender", "party": "jdName"}
    data = [
        councilor[factor_field[factor]]
        for councilor in client["council"]["national_councilor"].find()
    ]
    # print(f"{metroId} {factor}")
    # print(data)
    client["stats"].get_collection("diversity_index").update_one(
        {"national": True},
        {"$set": {f"{factor}DiversityIndex": gini_simpson(data, stair, opts)}},
        upsert=True,
    )


def calculate_age_diversity_rank_history_national() -> None:
    for is_elected in [True, False]:
        docs = client["stats"]["age_hist"].find(
            {
                "councilorType": "national_councilor",
                "method": "equal",
                "is_elected": is_elected,
            }
        )
        for doc in docs:
            diversity_index = gini_simpson(
                [
                    group["minAge"]
                    for group in doc["data"]
                    for _ in range(group["count"])
                ],
                stair=10,
            )
            client["stats"]["age_hist"].find_one_and_update(
                {
                    "councilorType": "national_councilor",
                    "method": "equal",
                    "is_elected": is_elected,
                    "year": doc["year"],
                },
                {"$set": {"diversityIndex": diversity_index}},
            )

        years = list({doc["year"] for doc in client["stats"]["age_hist"].find()})

        for year in years:
            result = client["stats"]["age_hist"].aggregate(
                [
                    {
                        "$match": {
                            "councilorType": "national_councilor",
                            "method": "equal",
                            "is_elected": is_elected,
                            "year": year,
                        }
                    },
                    {"$sort": {"diversityIndex": -1}},
                    {"$group": {"_id": "", "items": {"$push": "$$ROOT"}}},
                    {"$unwind": {"path": "$items", "includeArrayIndex": "items.rank"}},
                    {"$replaceRoot": {"newRoot": "$items"}},
                    {"$addFields": {"rank": {"$add": ["$rank", 1]}}},
                ]
            )
            for doc in result:
                client["stats"]["age_hist"].find_one_and_update(
                    {
                        "councilorType": "national_councilor",
                        "method": "equal",
                        "is_elected": is_elected,
                        "year": year,
                    },
                    {"$set": {"diversityRank": int(doc["rank"])}},
                )


def main():
    for localId in range(1, 227):
        save_to_mongo_local(localId, "age", stair=10)
        save_to_mongo_local(localId, "gender")
        save_to_mongo_local(localId, "party")
    calculate_rank_local("age")
    calculate_rank_local("gender")
    calculate_rank_local("party")
    calculate_age_diversity_rank_history_local()

    for metroId in range(1, 18):
        if metroId in [8, 17]:
            continue
        save_to_mongo_metro(metroId, "age", stair=10)
        save_to_mongo_metro(metroId, "gender")
        save_to_mongo_metro(metroId, "party")
    calculate_rank_metro("age")
    calculate_rank_metro("gender")
    calculate_rank_metro("party")
    calculate_age_diversity_rank_history_metro()

    save_to_mongo_national("age", stair=10)
    save_to_mongo_national("gender")
    save_to_mongo_national("party")
    calculate_age_diversity_rank_history_national()


if __name__ == "__main__":
    main()
