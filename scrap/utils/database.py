from typing import List

from db.client import client
from configurations.secrets import MongoDBSecrets

from db.types import CouncilType, Councilor
from scrap.utils.types import ScrapResult
from dataclasses import asdict
import json


def save_to_database(record: ScrapResult) -> bool:
    """
    지방의회 크롤링 결과를 데이터베이스에 저장합니다.
    :param record: 지방의회 크롤링 결과
    :return: 저장 성공 여부를 불리언 값으로 반환합니다.
    """
    db = client[str(MongoDBSecrets.database_name)]
    collection = db[str(record.council_type)]

    cid = record.council_id

    new_councilors = check_new_councilors(collection, record)
    resigned_councilors = check_resigned_councilors(collection, record)
    other_councilors = [
        councilor
        for councilor in record.councilors
        if councilor not in new_councilors
        and councilor.name
        not in [councilor["name"] for councilor in resigned_councilors]
    ]

    # TODO: DB에 없던 새로운 의원 핸들링
    update_councilors(collection, cid, other_councilors)
    remove_councilors(collection, resigned_councilors)
    add_councilors(collection, cid, new_councilors, str(record.council_type))

    return True


def check_new_councilors(collection, record: ScrapResult) -> list[Councilor]:
    """
    DB에 없던 새로운 의원을 찾아 반환합니다.
    :param collection: MongoDB 컬렉션
    :param record: 지방의회 크롤링 결과
    :return: 새로운 의원 목록
    """
    new_councilors = []

    for councilor in record.councilors:
        if (
            collection.find_one({"localId": record.council_id, "name": councilor.name})
            is None
        ):
            new_councilors.append(councilor)

    return new_councilors


def check_resigned_councilors(collection, record: ScrapResult) -> list[dict]:
    """
    DB에 있었으나 사퇴한 의원을 찾아 반환합니다.
    :param collection: MongoDB 컬렉션
    :param record: 지방의회 크롤링 결과
    :return: 사퇴한 의원 목록
    """
    resigned_councilors = []

    for councilor in collection.find({"localId": record.council_id}):
        if councilor["name"] not in [councilor.name for councilor in record.councilors]:
            resigned_councilors.append(councilor)

    return resigned_councilors


def update_councilors(collection, cid: int, councilors: List[Councilor]) -> None:
    """
    신규/사퇴 의원이 아닌 의원 정보를 업데이트합니다.
    :param collection: MongoDB 컬렉션
    :param councilors: 업데이트할 의원 리스트
    """
    for councilor in councilors:
        collection.update_one(
            {"localId": cid, "name": councilor.name},
            {"$set": asdict(councilor)},
            upsert=False,
        )


def remove_councilors(collection, councilors: List[Councilor]) -> None:
    """
    사퇴한 의원을 데이터베이스에서 제거합니다.
    :param collection: MongoDB 컬렉션
    :param councilors: 제거할 의원 리스트
    """
    for councilor in councilors:
        collection.delete_one(
            {"localId": councilor["localId"], "name": councilor["name"]}
        )

def add_councilors(collection, cid: int, councilors: List[Councilor], council_type: str) -> None:
    """
    신규 의원을 검사합니다. 기존 비례대표의 사퇴로 새 비례대표가 바로 추가되었을
    가능성을 보고, 아닐 시에는 사용자에게 보고합니다.
    :param collection: MongoDB 컬렉션
    :param councilors: 업데이트할 의원 리스트
    :param council_type: local_councilor 등등, 의원의 종류 
    """
    db = client[str(MongoDBSecrets.database_name)]
    candcoll = db[council_type + "_cand"] # 예: local_councilor_cand
    for councilor in councilors:
        # find the councilor in candidate
        query = {"localId": cid, "name": councilor.name}
        all_documents = list(candcoll.find(query))
        assert(len(all_documents) <= 1, "신규의원을 같은 의회의 후보중에 찾는데, 동명이인이 있네요.")
        if len(all_documents) == 0:
            # no candidate found, report to user
            print(f"신규의원 {councilor.name}을 찾을 수 없습니다.")
            continue
        found_document = all_documents[0]
        age = found_document.get("age")
        # birthday = found_document.get("birthday")
        councilor.age = age
        collection.update_one(
            {"localId": cid, "name": councilor.name},
            {"$set": asdict(councilor)},
            upsert=False,
        )