from unittest import mock, TestCase
import json
from main import app


@mock.patch.dict("os.environ", {"UNSPLASH_KEY": "test-key"})
@mock.patch("main.unsplash_client")
@mock.patch("main.images_collection")
class TestAPI(TestCase):
    def test_new_image_requests_image_using_query_param(self, _, unsplash_client):
        return_value = json.loads('{"test": "value"}')
        unsplash_client.get_new_image.return_value = return_value

        with app.test_client() as client:
            res = client.get("/new-image?query=test")

        unsplash_client.get_new_image.assert_called_with("test")
        assert res.json == return_value

    def test_get_images_retrieves_images_from_mongo(self, images_collection, _):
        return_value = json.loads('[{"test": "value"}, {"test2": "value2"}]')
        images_collection.find.return_value = return_value

        with app.test_client() as client:
            res = client.get("/images")

        images_collection.find.assert_called_with({})
        assert res.json == return_value

    def test_post_images_adds_images_to_mongo(self, images_collection, _):
        image_json = json.loads('{"test": "value", "id": "123"}')
        inserted_json = json.loads('{"test": "value", "id": "123", "_id": "123"}')
        return_value = json.loads('{"inserted_id": "123"}')
        images_collection.insert_one.return_value = MockMongoInsertionResult(
            inserted_id="123"
        )

        with app.test_client() as client:
            res = client.post("/images", json=image_json)

        images_collection.insert_one.assert_called_with(inserted_json)
        assert res.json == return_value

    def test_delete_images_removes_image_from_mongo_if_present(
        self, images_collection, _
    ):
        image_id = "123"
        delete_dict = {"_id": image_id}

        with app.test_client() as client:
            res = client.delete("/images/" + image_id)

        images_collection.delete_one.assert_called_with(delete_dict)
        assert res.json == json.loads('{"deleted_id": "123"}')

    def test_delete_images_returns_404_if_image_not_present(self, images_collection, _):
        image_id = "123"
        delete_dict = {"_id": image_id}
        images_collection.delete_one.return_value = MockMongoDeletionResult(
            deleted_count=0
        )

        with app.test_client() as client:
            res = client.delete("/images/" + image_id)

        images_collection.delete_one.assert_called_with(delete_dict)
        assert res.json == json.loads('{"error": "Image with Id 123 not found"}')
        assert res.status_code == 404

    def test_delete_images_returns_500_if_mongo_returns_none(
        self, images_collection, _
    ):
        image_id = "123"
        delete_dict = {"_id": image_id}
        images_collection.delete_one.return_value = None

        with app.test_client() as client:
            res = client.delete("/images/" + image_id)

        images_collection.delete_one.assert_called_with(delete_dict)
        assert res.json == json.loads(
            '{"error": "Image was not deleted. Please try again"}'
        )
        assert res.status_code == 500


class MockMongoInsertionResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class MockMongoDeletionResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count
