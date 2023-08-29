import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from mongo_client import client as mongo_client

gallery = mongo_client.gallery
images_collection = gallery.images

load_dotenv(dotenv_path="./api/.env.local")

UNSPLASH_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_KEY = os.environ.get("UNSPLASH_KEY", "")

if not UNSPLASH_KEY:
    raise EnvironmentError("Please provide UNSPLASH_KEY in .env.local file")

app = Flask(__name__)
CORS(app)


@app.route("/new-image")
def new_image():
    """retrieve new image from Unsplash"""
    word = request.args.get("query")
    response = requests.get(
        UNSPLASH_URL,
        headers={"Accept-Version": "v1", "Authorization": f"Client-ID {UNSPLASH_KEY}"},
        params={"query": word},
        timeout=10,
    )

    data = response.json()
    return data


@app.route("/images")
def images():
    """Store and retrieve images from mongo"""
    if request.method == "GET":
        image_data = images_collection.find({})
        return jsonify([img for img in image_data])

    if request.method == "POST":
        image = request.get_json()
        image["_id"] = image.get("id")
        result = images_collection.insert_one(image)
        return {"inserted_id": result.inserted_id}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
