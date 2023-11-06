from db.client import client
from configurations.secrets import MongoDBSecrets
from scrap.utils.types import CouncilType, Councilor, ScrapResult
import dataclasses
import json

# Note: MongoDB는 데이터베이스가 존재하지 않으면 자동으로 생성합니다.
# MongoDB 데이터베이스는 하나 이상의 컬렉션으로 구성됩니다.
# 컬렉션은 하나 이상의 문서로 구성됩니다.
db = client[str(MongoDBSecrets.database_name)]


def save_to_database(record: ScrapResult):
    """
    지방의회 크롤링 결과를 데이터베이스에 저장합니다.
    각 의회의 기존 데이터는 덮어 씌워집니다.
    예시는 scrap/utils/database.py를 참조해주세요.
    :param record: 지방의회 크롤링 결과
    :return: 저장 성공 여부를 불리언 값으로 반환합니다.
    """
    try:
        # MongoDB는 JSON을 저장할 수 있습니다.
        # JSON 형태로 변환한 후, MongoDB에 저장합니다.
        # serialized_record = json.dumps(dataclasses.asdict(record), ensure_ascii=False)
        collection = db[str(record.council_type)]
        result = collection.find_one(
            {"councilId": record.council_id},
        )
        if result is not None:
            collection.delete_one({"councilId": record.council_id})

            updated_array = []
            for councilor in record.councilors:
                for before_councilor in result:
                    if councilor.name == before_councilor['name']:
                        before_councilor['party'] = councilor.party
                        updated_array.append(before_councilor)
            
            collection.find_one_and_update(
                {"councilId": record.council_id},
                {"$set": {
                    "councilors" : updated_array
                }}, upsert=True
            )
        else:
            return False
                    
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == "__main__":
    test_record = ScrapResult(
        council_id="test-test",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=[
            Councilor(name="김철수", party="국민의힘"),
            Councilor(name="김영희", party="더불어민주당"),
        ],
    )
    print(save_to_database(test_record))
