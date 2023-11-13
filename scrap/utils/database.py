from db.client import client
from configurations.secrets import MongoDBSecrets

from db.types import CouncilType, Councilor
from scrap.utils.types import ScrapResult
from dataclasses import asdict
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
            {"council_id": record.council_id},
        )
        if result is not None:
            before_councilors = result["councilors"]  # List[dict]
            updated_councilors = []
            updated_names = set()

            name_data_map_for_update = {d.name: asdict(d) for d in record.councilors}

            for d in before_councilors:
                if d["name"] in name_data_map_for_update:
                    d.update(
                        {
                            k: v
                            for k, v in name_data_map_for_update[d["name"]].items()
                            if k in d
                        }
                    )
                    updated_names.add(d["name"])
                updated_councilors.append(d)

            for d in record.councilors:
                if d.name not in updated_names:
                    updated_councilors.append(asdict(d))

            collection.find_one_and_update(
                {"council_id": record.council_id},
                {"$set": {"councilors": updated_councilors}},
                upsert=True,
            )
        else:
            return False

        return True
    except Exception as e:
        t
        print(e)
        return False


if __name__ == "__main__":
    test_record = ScrapResult(
        council_id="test-test",
        council_type=CouncilType.LOCAL_COUNCIL,
        councilors=[
            Councilor(name="김철수", jdName="국민의힘"),
            Councilor(name="김영희", jdName="Birthday Party"),
            Councilor(name="테스트", jdName="테스트당"),
        ],
    )
    print(save_to_database(test_record))
