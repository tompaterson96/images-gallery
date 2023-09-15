import json
from unittest.mock import patch, AsyncMock
from main import app
import pytest


class MockMongoInsertionResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id


class MockMongoDeletionResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count


@pytest.mark.parametrize("word", ["car", "bus", "train"])
# @patch("main.unsplash_client")
def test_new_image_requests_image_using_query_param(word):
    mock_get_new_image = AsyncMock()
    with patch("main.unsplash_client.get_new_image", side_effect=mock_get_new_image):
        return_value = json.loads('{"test": "value"}')
        # unsplash_client.get_new_image.return_value = return_value
        mock_get_new_image.return_value = return_value

        with app.test_client() as client:
            res = client.get(f"/new-image?query={word}")

        # unsplash_client.get_new_image.assert_called_with(word)
        mock_get_new_image.assert_called_with(word)
        assert res.json == return_value


@patch("main.images_collection")
def test_get_images_retrieves_images_from_mongo(images_collection):
    return_value = json.loads('[{"test": "value"}, {"test2": "value2"}]')
    images_collection.find.return_value = return_value

    with app.test_client() as client:
        res = client.get("/images")

    images_collection.find.assert_called_with({})
    assert res.json == return_value


@patch("main.images_collection")
def test_post_images_adds_images_to_mongo(
    images_collection,
):
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


@pytest.mark.parametrize(
    "deletion_result, status_code, expected_response_json",
    [
        (MockMongoDeletionResult(1), 200, json.loads('{"deleted_id": "123"}')),
        (
            MockMongoDeletionResult(0),
            404,
            json.loads('{"error": "Image with Id 123 not found"}'),
        ),
        (
            None,
            500,
            json.loads('{"error": "Image was not deleted. Please try again"}'),
        ),
    ],
)
@patch("main.images_collection")
def test_delete_images_removes_image_from_mongo_if_present(
    images_collection, deletion_result, status_code, expected_response_json
):
    image_id = "123"
    delete_dict = {"_id": image_id}
    images_collection.delete_one.return_value = deletion_result

    with app.test_client() as client:
        res = client.delete("/images/" + image_id)

    images_collection.delete_one.assert_called_with(delete_dict)
    assert res.status_code == status_code
    assert res.json == expected_response_json
