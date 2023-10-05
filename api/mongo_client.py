import os
import pymongo
from dotenv import load_dotenv

load_dotenv(dotenv_path="./api/.env.local")

MONGO_URL = os.environ.get("MONGO_URL", "mongo")
MONGO_PORT = os.environ.get("MONGO_PORT", 27017)
MONGO_USERNAME = os.environ.get("MONGO_USERNAME", "root")
MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD", "")

client = pymongo.MongoClient(
    host=MONGO_URL,
    port=MONGO_PORT,
    username=MONGO_USERNAME,
    password=MONGO_PASSWORD,
)


def insert_test_document():
    db = client.test
    test_collection = db.test_collection
    res = test_collection.insert_one({"name": "Tom", "company": "bjss"})
    print(res)
