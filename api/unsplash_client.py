import os
import requests
from dotenv import load_dotenv

env_file = "./api/.env.local"
for root, dirnames, filenames in os.walk(os.getcwd()):
    for file in filenames:
        if file == ".env.local":
            env_file = os.path.join(root, file)
            break

load_dotenv(dotenv_path=env_file)

UNSPLASH_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_KEY = os.environ.get("UNSPLASH_KEY", "")

if not UNSPLASH_KEY:
    raise EnvironmentError("Please provide UNSPLASH_KEY in .env.local file")


def get_new_image(word):
    response = requests.get(
        UNSPLASH_URL,
        headers={"Accept-Version": "v1", "Authorization": f"Client-ID {UNSPLASH_KEY}"},
        params={"query": word},
        timeout=10,
    )

    return response.json()
