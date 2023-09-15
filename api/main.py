from flask import Flask, request, jsonify
from flask_cors import CORS
import unsplash_client
from mongo_client import client as mongo_client

gallery = mongo_client.gallery
images_collection = gallery.images

app = Flask(__name__)
CORS(app)


@app.route("/new-image")
async def new_image():
    """retrieve new image from Unsplash"""
    word = request.args.get("query")
    response = await unsplash_client.get_new_image(word)
    return response


@app.route("/images", methods=["GET", "POST"])
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


@app.route("/images/<image_id>", methods=["DELETE"])
def image_by_id(image_id):
    """Delete image from mongo"""
    result = images_collection.delete_one({"_id": image_id})
    if not result:
        return {"error": "Image was not deleted. Please try again"}, 500
    if result and not result.deleted_count:
        return {"error": f"Image with Id {image_id} not found"}, 404
    return {"deleted_id": image_id}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
