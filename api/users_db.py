import uuid
import bcrypt
from mongo_client import client as mongo_client


class UserDatabase:
    def __init__(self):
        gallery = mongo_client.gallery
        self._users_collection = gallery.users

    def register(self, email, password, name):
        if self._users_collection.find_one({"email": email}):
            return {"error": "User already registered with email provided"}
        pwd_hash = self._hash_password(password)
        new_user = {
            "_id": str(uuid.uuid4()),
            "email": email,
            "password": pwd_hash,
            "name": name,
        }
        self._users_collection.insert_one(new_user)
        del new_user["password"]
        return new_user

    def login(self, email, password):
        user = self._users_collection.find_one({"email": email})
        if not user:
            return {"error": "No user registered with email provided"}
        pwd_bytes = password.encode("utf-8")
        if not bcrypt.checkpw(pwd_bytes, user["password"]):
            return {"error": "Incorrect email or password"}
        del user["password"]
        return user

    def _hash_password(self, password):
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd_bytes, salt)
