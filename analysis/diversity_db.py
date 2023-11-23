from collections import Counter
import math
from pymongo.operations import UpdateOne

from db.client import client


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


def save_to_mongo(localId: int, factor: str, stair=0, opts=False) -> None:
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


def calculate_rank(factor: str) -> None:
    result = client["stats"]["diversity_index"].aggregate(
        [
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


if __name__ == "__main__":
    for localId in range(1, 227):
        save_to_mongo(localId, "age", stair=10)
        save_to_mongo(localId, "gender")
        save_to_mongo(localId, "party")
    calculate_rank("age")
    calculate_rank("gender")
    calculate_rank("party")
