from mongo_client import client as mongo_client


class ImageDatabase:
    def __init__(self):
        gallery = mongo_client.gallery
        self._images_collection = gallery.images

    def get_all_images_for_user(self, user_id):
        image_data = self._images_collection.find({"saved_by_users": user_id})
        return [img for img in image_data]

    def save_image_for_user(self, image, user_id):
        image_id = image.get("id")
        image_data = self._images_collection.find_one({"_id": image_id})

        if image_data:
            result = self._images_collection.update_one(
                {"_id": image_id}, {"$push": {"saved_by_users": user_id}}
            )
            return {"inserted_id": result.modified_count}
        else:
            image["_id"] = image.get("id")
            image["saved_by_users"] = [user_id]
            print(image)
            result = self._images_collection.insert_one(image)
            return {"inserted_id": result.inserted_id}

    def delete_image_for_user(self, image_id, user_id):
        image_data = self._images_collection.find_one({"_id": image_id})

        if image_data:
            result = self._images_collection.update_one(
                {"_id": image_id}, {"$pull": {"saved_by_users": user_id}}
            )
            return {"deleted_count": result.modified_count}
        else:
            result = self._images_collection.delete_one({"_id": image_id})
            return {"deleted_count": result.deleted_count}
