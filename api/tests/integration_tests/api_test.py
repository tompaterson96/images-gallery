import json
from unittest.mock import patch, AsyncMock
import main
from main import app
import pytest
import mongomock


def setup_function():
    print("setup")
    main.users_db._users_collection = mongomock.MongoClient().gallery.users_collection
    main.users_db._users_collection.insert_one(
        {
            "_id": "A",
            "email": "test.user@bjss.com",
            "name": "dev",
            "password": main.users_db._hash_password("password"),
        }
    )

    main.images_db._images_collection = (
        mongomock.MongoClient().gallery.images_collection
    )
    main.images_db._images_collection.insert_many(
        [
            {"_id": "1", "test": "value1", "saved_by_users": ["A"]},
            {"_id": "2", "test": "value2", "saved_by_users": ["B"]},
            {"_id": "3", "test": "value3", "saved_by_users": ["A", "B"]},
        ]
    )


def teardown_function():
    print("teardown")
    main.images_db._images_collection.drop()


@pytest.mark.parametrize("word", ["car", "bus", "train"])
def test_new_image_requests_image_using_query_param(word):
    mock_unsplash_image = AsyncMock()
    with patch("main.unsplash_client.get_new_image", side_effect=mock_unsplash_image):
        return_value = json.loads('{"test": "value"}')
        mock_unsplash_image.return_value = return_value

        with app.test_client() as client:
            res = client.get(f"/new-image?query={word}")

        mock_unsplash_image.assert_called_with(word)
        assert res.json == return_value


def test_images_endpoint_requires_login():
    with app.test_client() as client:
        res = client.get("/images")

    assert res.status_code == 401
    response = res.json
    assert "msg" in response
    assert response["msg"] == "Missing Authorization Header"


def test_get_images_retrieves_images_saved_by_user_from_mongo():
    with app.test_client() as client:
        token = client.post(
            "/token", json={"email": "test.user@bjss.com", "password": "password"}
        )
        header = {"Authorization": f"Bearer {token.json['access_token']}"}
        res = client.get("/images", headers=header)

    assert res.status_code == 200
    response = res.json
    assert len(response) == 2
    assert "1" in [image["_id"] for image in response]
    assert "3" in [image["_id"] for image in response]


def test_post_images_saves_new_image_for_user_in_mongo():
    image = {"id": "2", "test": "value2"}
    with app.test_client() as client:
        token = client.post(
            "/token", json={"email": "test.user@bjss.com", "password": "password"}
        )
        header = {"Authorization": f"Bearer {token.json['access_token']}"}
        res = client.post("/images", json=image, headers=header)

    assert res.status_code == 200
    response = res.json
    assert response["inserted_id"] == "2"

    stored_image = main.images_db._images_collection.find_one({"_id": "2"})
    assert stored_image
    assert "A" in stored_image["saved_by_users"]


def test_post_images_does_nothing_if_user_already_saved_image_in_mongo():
    image = {"id": "1", "test": "value1"}
    with app.test_client() as client:
        token = client.post(
            "/token", json={"email": "test.user@bjss.com", "password": "password"}
        )
        header = {"Authorization": f"Bearer {token.json['access_token']}"}
        res = client.post("/images", json=image, headers=header)

    assert res.status_code == 200
    response = res.json
    assert response["inserted_id"] == "1"

    stored_image = main.images_db._images_collection.find_one({"_id": "1"})
    assert stored_image
    assert stored_image["saved_by_users"] == ["A"]


def test_image_by_id_endpoint_requires_login():
    with app.test_client() as client:
        res = client.delete("/images/1")

    assert res.status_code == 401
    response = res.json
    assert "msg" in response
    assert response["msg"] == "Missing Authorization Header"


def test_delete_image_by_id_removes_image_for_user_in_mongo():
    with app.test_client() as client:
        token = client.post(
            "/token", json={"email": "test.user@bjss.com", "password": "password"}
        )
        header = {"Authorization": f"Bearer {token.json['access_token']}"}
        res = client.delete("/images/1", headers=header)

    assert res.status_code == 200
    response = res.json
    assert response["deleted_id"] == "1"

    stored_image = main.images_db._images_collection.find_one({"_id": "1"})
    assert not stored_image


def test_delete_image_by_id_does_nothing_for_image_not_saved_by_user_in_mongo():
    with app.test_client() as client:
        token = client.post(
            "/token", json={"email": "test.user@bjss.com", "password": "password"}
        )
        header = {"Authorization": f"Bearer {token.json['access_token']}"}
        res = client.delete("/images/2", headers=header)

    assert res.status_code == 404
    response = res.json
    assert response["error"] == "Image with Id 2 not found"

    stored_image = main.images_db._images_collection.find_one({"_id": "2"})
    assert stored_image
    assert "A" not in stored_image["saved_by_users"]


def test_delete_account_endpoint_requires_login():
    with app.test_client() as client:
        res = client.delete("/delete-account")

    assert res.status_code == 401
    response = res.json
    assert "msg" in response
    assert response["msg"] == "Missing Authorization Header"


def test_delete_account_removes_images_for_user_in_mongo():
    with app.test_client() as client:
        token = client.post(
            "/token", json={"email": "test.user@bjss.com", "password": "password"}
        )
        header = {"Authorization": f"Bearer {token.json['access_token']}"}
        res = client.delete("/delete-account", headers=header)

    assert res.status_code == 200
    response = res.json
    assert response["images"]["deleted_count"] == 2

    stored_images = main.images_db._images_collection.find({"saved_by_users": "A"})
    assert not [img for img in stored_images]


def test_delete_account_removes_user_from_mongo():
    with app.test_client() as client:
        token = client.post(
            "/token", json={"email": "test.user@bjss.com", "password": "password"}
        )
        header = {"Authorization": f"Bearer {token.json['access_token']}"}
        res = client.delete("/delete-account", headers=header)

    assert res.status_code == 200
    response = res.json
    assert response["user"]["deleted_count"] == 1

    stored_user = main.users_db._users_collection.find_one({"_id": "A"})
    assert not stored_user


# @patch("main.images_collection")
# def test_post_images_adds_images_to_mongo(
#     images_collection,
# ):
#     image_json = json.loads('{"test": "value", "id": "123"}')
#     inserted_json = json.loads('{"test": "value", "id": "123", "_id": "123"}')
#     return_value = json.loads('{"inserted_id": "123"}')
#     images_collection.insert_one.return_value = MockMongoInsertionResult(
#         inserted_id="123"
#     )

#     with app.test_client() as client:
#         res = client.post("/images", json=image_json)

#     images_collection.insert_one.assert_called_with(inserted_json)
#     assert res.json == return_value


# @pytest.mark.parametrize(
#     "deletion_result, status_code, expected_response_json",
#     [
#         (MockMongoDeletionResult(1), 200, json.loads('{"deleted_id": "123"}')),
#         (
#             MockMongoDeletionResult(0),
#             404,
#             json.loads('{"error": "Image with Id 123 not found"}'),
#         ),
#         (
#             None,
#             500,
#             json.loads('{"error": "Image was not deleted. Please try again"}'),
#         ),
#     ],
# )
# @patch("main.images_collection")
# def test_delete_images_removes_image_from_mongo_if_present(
#     images_collection, deletion_result, status_code, expected_response_json
# ):
#     image_id = "123"
#     delete_dict = {"_id": image_id}
#     images_collection.delete_one.return_value = deletion_result

#     with app.test_client() as client:
#         res = client.delete("/images/" + image_id)

#     images_collection.delete_one.assert_called_with(delete_dict)
#     assert res.status_code == status_code
#     assert res.json == expected_response_json
