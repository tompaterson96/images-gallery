from images_db import ImageDatabase
import mongomock
import pytest  # needed to run tests in Test Explorer

images_db = ImageDatabase()
images_db._images_collection = mongomock.MongoClient().gallery.images_collection
images_collection = images_db._images_collection


def setup_function():
    print("setup")
    images_collection.insert_many(
        [
            {"_id": "1", "test": "value1", "saved_by_users": ["A"]},
            {"_id": "2", "test": "value2", "saved_by_users": ["B"]},
            {"_id": "3", "test": "value3", "saved_by_users": ["A", "B"]},
        ]
    )


def teardown_function():
    print("teardown")
    images_collection.drop()


def test_get_all_images_for_user_with_no_images_in_mongo_returns_empty_list():
    results = images_db.get_all_images_for_user("C")

    assert len(results) == 0


def test_get_all_images_for_user_retrieves_images_from_mongo():
    results = images_db.get_all_images_for_user("A")

    assert len(results) == 2
    assert any([result["test"] == "value1" for result in results])
    assert any([result["test"] == "value3" for result in results])


def test_save_image_for_user_with_new_image_adds_entry_to_mongo():
    image = {"id": "4", "test": "value4"}

    result = images_db.save_image_for_user(image, "A")

    assert result["inserted_id"] == "4"

    saved_image = images_collection.find_one({"_id": "4"})
    assert saved_image["test"] == "value4"
    assert len(saved_image["saved_by_users"]) == 1
    assert saved_image["saved_by_users"][0] == "A"


def test_save_image_for_user_with_existing_image_adds_user_to_image_in_mongo():
    image = {"id": "2", "test": "value2"}

    result = images_db.save_image_for_user(image, "A")

    assert result["inserted_id"] == "2"

    saved_image = images_collection.find_one({"_id": "2"})
    assert saved_image["test"] == "value2"
    assert len(saved_image["saved_by_users"]) == 2
    assert any([user_id != "A" for user_id in saved_image["saved_by_users"]])
    assert any([user_id == "A" for user_id in saved_image["saved_by_users"]])


def test_delete_image_for_user_with_image_not_in_mongo_is_handled():
    result = images_db.delete_image_for_user("5", "A")

    assert result["deleted_count"] == 0


def test_delete_image_for_user_with_image_saved_in_mongo_by_user_is_handled():
    result = images_db.delete_image_for_user("2", "A")

    assert result["deleted_count"] == 1


def test_delete_image_for_user_with_image_saved_by_single_user_removes_entry_from_mongo():
    image_id = "1"

    result = images_db.delete_image_for_user(image_id, "A")

    assert result["deleted_count"] == 1

    deleted_image = images_collection.find_one({"_id": image_id})
    assert not deleted_image


def test_delete_image_for_user_with_image_saved_by_multiple_users_removes_user_from_image_in_mongo():
    image_id = "3"

    result = images_db.delete_image_for_user(image_id, "A")

    assert result["deleted_count"] == 1

    deleted_image = images_collection.find_one({"_id": image_id})
    assert deleted_image["test"] == "value3"
    assert len(deleted_image["saved_by_users"]) == 1
    assert all([user_id != "A" for user_id in deleted_image["saved_by_users"]])


def test_delete_all_images_for_user_with_no_images_in_mongo():
    result = images_db.delete_all_images_for_user("C")

    assert result["deleted_count"] == 0


def test_delete_all_images_for_user_removes_user_from_images_in_mongo():
    result = images_db.delete_all_images_for_user("A")

    assert result["deleted_count"] == 2

    remaining_images = [img for img in images_collection.find()]
    assert all(
        [
            user_id != "A"
            for user_id in [image["saved_by_users"] for image in remaining_images]
        ]
    )
