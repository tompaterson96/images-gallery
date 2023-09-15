from unittest import mock, TestCase, main
import json
from main import app
from parameterized import parameterized


class MockMongoInsertionResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class MockMongoDeletionResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


@mock.patch("main.unsplash_client")
@mock.patch("main.images_collection")
class TestAPI(TestCase):
    @parameterized.expand(["car", "bus", "train"])
    async def test_new_image_requests_image_using_query_param(
        self, _, unsplash_client, word
    ):
        return_value = json.loads('{"test": "value"}')
        unsplash_client.get_new_image.return_value = return_value

        with app.test_client() as client:
            res = client.get(f"/new-image?query={word}")

        unsplash_client.get_new_image.assert_called_with(word)
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

    @parameterized.expand(
        [
            [MockMongoDeletionResult(1), 200, json.loads('{"deleted_id": "123"}')],
            [
                MockMongoDeletionResult(0),
                404,
                json.loads('{"error": "Image with Id 123 not found"}'),
            ],
            [
                None,
                500,
                json.loads('{"error": "Image was not deleted. Please try again"}'),
            ],
        ]
    )
    def test_delete_images_removes_image_from_mongo_if_present(
        self, images_collection, _, deletion_result, status_code, expected_response_json
    ):
        image_id = "123"
        delete_dict = {"_id": image_id}
        images_collection.delete_one.return_value = deletion_result

        with app.test_client() as client:
            res = client.delete("/images/" + image_id)

        images_collection.delete_one.assert_called_with(delete_dict)
        assert res.status_code == status_code
        assert res.json == expected_response_json


if __name__ == "__main__":
    main()
