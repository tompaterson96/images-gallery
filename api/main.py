from datetime import datetime, timezone, timedelta
import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required,
    JWTManager,
)

import unsplash_client
from users_db import UserDatabase
from images_db import ImageDatabase

users_db = UserDatabase()
images_db = ImageDatabase()

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
jwt = JWTManager(app)


@app.route("/token", methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = users_db.login(email, password)
    if "error" in user:
        return user, 400

    access_token = create_access_token(identity=user)
    user = {"access_token": access_token}
    return user


@app.route("/register", methods=["POST"])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    name = request.json.get("name", None)
    if not email or not password or not name:
        return {"error": "All details must be provided"}, 404

    user = users_db.register(email, password, name)
    if "error" in user:
        return user, 409

    access_token = create_access_token(identity=user)
    response = {"access_token": access_token}
    return response


@app.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=15))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if isinstance(data, dict):
                data["access_token"] = access_token
                response.data = json.dumps(data)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response


@app.route("/new-image")
async def new_image():
    """retrieve new image from Unsplash"""
    word = request.args.get("query")
    response = await unsplash_client.get_new_image(word)
    return response


@app.route("/images", methods=["GET", "POST"])
@jwt_required()
def images():
    """Store and retrieve images from mongo"""
    if request.method == "GET":
        return jsonify(images_db.get_all_images())

    if request.method == "POST":
        image = request.get_json()
        return images_db.save_image(image)


@app.route("/images/<image_id>", methods=["DELETE"])
@jwt_required()
def image_by_id(image_id):
    """Delete image from mongo"""
    result = images_db.delete_image(image_id)
    if not result:
        return {"error": "Image was not deleted. Please try again"}, 500
    if result and not result.deleted_count:
        return {"error": f"Image with Id {image_id} not found"}, 404
    return {"deleted_id": image_id}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
