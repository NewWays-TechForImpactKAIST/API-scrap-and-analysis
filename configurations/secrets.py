"""
데이터베이스 연결 및 API 호출에 필요한 비밀 정보를 정의합니다.
"""
import os
from dotenv import load_dotenv

# .env 파일로부터 환경변수를 불러옵니다.
load_dotenv(verbose=False, override=False)


class MongoDBSecrets:
    """
    MongoDB 연결을 위한 연결 정보를 정의합니다.
    """

    connection_uri = str(
        os.getenv("MONGO_CONNECTION_URI") or "mongodb://localhost:27017"
    )
    """PyMongo 클라이언트에서 데이터베이스 연결에 사용할 연결 uri입니다."""
    database_name = str(os.getenv("MONGO_DATABASE") or "local")
    """PyMongo 클라이언트에서 사용할 데이터베이스 이름입니다."""


class OpenDataPortalSecrets:
    """
    공공데이터포털(data.go.kr) API 호출에 필요한 서비스 키를 정의합니다.
    """

    service_key = str(os.getenv("OPEN_DATA_SERICE_KEY") or "")


class EmailSecrets:
    """
    스크랩 결과 이메일 전송에 필요한 키를 정의합니다.
    """

    sender_email = str(os.getenv("SCRAP_SENDER_EMAIL") or "")
    receiver_email = str(os.getenv("SCRAP_RECEIVER_EMAIL") or "")
    password = str(os.getenv("SCRAP_EMAIL_PASSWORD") or "")
