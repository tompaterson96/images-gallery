import unittest
from unittest import mock
import mongo_client


class TestMongoClient(unittest.TestCase):
    @mock.patch("mongo_client.client")
    def test_insert_test_document(self, client):
        mongo_client.insert_test_document()
        client.test.test_collection.insert_one.assert_called_once()


if __name__ == "__main__":
    unittest.main()
