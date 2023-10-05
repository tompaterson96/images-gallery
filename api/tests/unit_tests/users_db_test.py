from users_db import UserDatabase
import mongomock
import pytest  # needed to run tests in Test Explorer

users_db = UserDatabase()
users_db._users_collection = mongomock.MongoClient().gallery.user_collection
users_collection = users_db._users_collection

password = "password"


def setup_function():
    print("setup")
    users_collection.insert_many(
        [
            {
                "_id": "1",
                "email": "test.user@bjss.com",
                "name": "dev",
                "password": UserDatabase._hash_password(password),
            }
        ]
    )


def teardown_function():
    print("teardown")
    users_collection.drop()


def test_register_with_existing_email_returns_error():
    result = users_db.register("test.user@bjss.com", "password", "new dev")
    assert "error" in result
    assert result["error"] == "User already registered with email provided"


def test_register_with_new_email_returns_user_without_password():
    result = users_db.register("tester@bjss.com", "password", "qa")
    assert "error" not in result
    assert result["email"] == "tester@bjss.com"
    assert result["name"] == "qa"
    assert "password" not in result


def test_login_with_invalid_email_returns_error():
    result = users_db.login("tester@bjss.com", "password")
    assert "error" in result
    assert result["error"] == "No user registered with email provided"


def test_login_with_invalid_password_returns_error():
    result = users_db.login("test.user@bjss.com", "wrong_password")
    assert "error" in result
    assert result["error"] == "Incorrect email or password"


def test_login_with_valid_email_and_password_returns_user_without_password():
    result = users_db.login("test.user@bjss.com", password)
    assert "error" not in result
    assert result["email"] == "test.user@bjss.com"
    assert result["name"] == "dev"
    assert "password" not in result


def test_derigister_with_invalid_id_returns_error():
    result = users_db.deregister("2")
    assert "error" in result
    assert result["error"] == "User not registered"


def test_derigister_with_valid_id_returns_deleted_count():
    result = users_db.deregister("1")
    assert "error" not in result
    assert result["deleted_count"] == 1
