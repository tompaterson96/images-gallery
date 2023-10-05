import unittest
from unittest import mock
import mongo_client
import mongomock


def test_insert_test_document_calls_adds_doc_to_mongo():
    mongo_client.client = mongomock.MongoClient()
    mongo_client.insert_test_document()

    docs = [doc for doc in mongo_client.client.test.test_collection.find()]
    assert len(docs) == 1


@mock.patch("mongo_client.client")
def test_insert_test_document_calls_insert_one(client):
    mongo_client.insert_test_document()
    client.test.test_collection.insert_one.assert_called_once()


if __name__ == "__main__":
    unittest.main()
