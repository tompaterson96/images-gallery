from mongo_client import client


class ImageDatabase:
    def __init__(self):
        gallery = client.gallery
        self._images_collection = gallery.images

    def get_all_images_for_user(self, user_id):
        image_data = self._images_collection.find({"saved_by_users": user_id})
        return [img for img in image_data]

    def save_image_for_user(self, image, user_id):
        image_id = image.get("id")
        image_data = self._images_collection.find_one({"_id": image_id})

        if image_data:
            if user_id in image_data["saved_by_users"]:
                return {"inserted_id": image_id}

            result = self._images_collection.update_one(
                {"_id": image_id}, {"$push": {"saved_by_users": user_id}}
            )
            return {"inserted_id": (image_id if result.modified_count else "")}
        else:
            image["_id"] = image.get("id")
            image["saved_by_users"] = [user_id]
            result = self._images_collection.insert_one(image)
            return {"inserted_id": result.inserted_id}

    def delete_image_for_user(self, image_id, user_id):
        image_data = self._images_collection.find_one(
            {"_id": image_id, "saved_by_users": user_id}
        )

        if not image_data:
            return {"deleted_count": 0}

        if len(image_data["saved_by_users"]) > 1:
            result = self._images_collection.update_one(
                {"_id": image_id}, {"$pull": {"saved_by_users": user_id}}
            )
            return {"deleted_count": result.modified_count}
        else:
            result = self._images_collection.delete_one({"_id": image_id})
            return {"deleted_count": result.deleted_count}

    def delete_all_images_for_user(self, user_id):
        response = {"deleted_count": 0}
        images_data = self._images_collection.find({"saved_by_users": user_id})

        for image in images_data:
            if len(image["saved_by_users"]) > 1:
                result = self._images_collection.update_one(
                    {"_id": image["_id"]}, {"$pull": {"saved_by_users": user_id}}
                )
                response["deleted_count"] += result.modified_count
            else:
                result = self._images_collection.delete_one({"_id": image["_id"]})
                response["deleted_count"] += result.deleted_count

        return response
