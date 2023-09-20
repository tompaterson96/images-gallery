from mongo_client import client as mongo_client


class ImageDatabase:
    def __init__(self):
        gallery = mongo_client.gallery
        self._images_collection = gallery.images

    def get_all_images(self):
        image_data = self._images_collection.find({})
        return [img for img in image_data]

    def save_image(self, image):
        image["_id"] = image.get("id")
        result = self._images_collection.insert_one(image)
        return {"inserted_id": result.inserted_id}

    def delete_image(self, image_id):
        return self._images_collection.delete_one({"_id": image_id})
