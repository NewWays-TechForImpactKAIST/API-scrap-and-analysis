"""
스크립트 실행에 필요한 환경변수를 정의합니다.
환경변수는 프로젝트 루트 폴더에 .env 파일을 생성하여 불러올 수 있습니다.
"""
import os
from dotenv import load_dotenv

# .env 파일로부터 환경변수를 불러옵니다.
load_dotenv(
    verbose=False,
    override=False
)

class MongoDBConfigurations:
    """
    MongoDB 연결을 위한 연결 정보를 정의합니다.
    """
    connection_uri = str(os.getenv("MONGO_CONNECTION_URI") or "mongodb://localhost:27017")
    """PyMongo 클라이언트에서 데이터베이스 연결에 사용할 연결 uri입니다."""


if __name__ == '__main__':
    print(MongoDBConfigurations.connection_uri)