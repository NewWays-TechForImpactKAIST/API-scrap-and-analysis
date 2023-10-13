import pymongo
from configurations.secrets import MongoDBSecrets

client = pymongo.MongoClient(MongoDBSecrets.connection_uri)
"""
MongoDB 클라이언트 객체입니다.
"""
