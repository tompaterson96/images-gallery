from main import app, jwt
from pytest import mark
from unittest import mock
from flask_jwt_extended import decode_token


@mock.patch("main.users_db.login", return_value={"error": "login failed"})
def test_create_token_while_login_returns_error_returns_BadRequest_and_error_message(_):
    user = {"email": "", "password": ""}
    with app.test_client() as client:
        res = client.post("/token", json=user)

    assert res.status_code == 400
    assert res.json == {"error": "login failed"}


@mock.patch(
    "main.users_db.login",
    return_value={"email": "test.user@bjss.com", "password": "", "name": "dev"},
)
def test_create_token_while_login_returns_token_returns_Ok_and_access_token(_):
    with app.test_client() as client:
        res = client.post(
            "/token", json={"email": "test.user@bjss.com", "password": ""}
        )

        assert res.status_code == 200
        token = res.json["access_token"]
        assert token
        decoded_token = decode_token(token)
        assert decoded_token["sub"]["name"] == "dev"
        assert decoded_token["sub"]["email"] == "test.user@bjss.com"


@mark.parametrize(
    "user",
    [
        {"email": "tester@bjss.com", "password": "password"},
        {"email": "tester@bjss.com", "name": "qa"},
        {"password": "password", "name": "qa"},
    ],
)
def test_register_with_missing_field_returns_BadRequest_and_error_message(user):
    with app.test_client() as client:
        res = client.post("/register", json=user)

    assert res.status_code == 400
    assert res.json == {"error": "All details must be provided"}


@mock.patch("main.users_db.register", return_value={"error": "register failed"})
def test_register_while_register_returns_error_returns_Conflict_and_error_message(_):
    user = {"email": "test.user@bjss.com", "password": "password", "name": "dev"}
    with app.test_client() as client:
        res = client.post("/register", json=user)

    assert res.status_code == 409
    assert res.json == {"error": "register failed"}


@mock.patch(
    "main.users_db.register",
    return_value={"email": "test.user@bjss.com", "name": "dev"},
)
def test_register_with_valid_new_user_returns_Ok_and_access_token_and_adds_user_to_database(
    _,
):
    user = {"email": "test.user@bjss.com", "password": "password", "name": "dev"}
    with app.test_client() as client:
        res = client.post("/register", json=user)

        assert res.status_code == 200
        token = res.json["access_token"]
        assert token
        decoded_token = decode_token(token)
        assert decoded_token["sub"]["name"] == "dev"
        assert decoded_token["sub"]["email"] == "test.user@bjss.com"


def test_logout_returns_Ok():
    with app.test_client() as client:
        res = client.post("/logout")
        assert res.status_code == 200
