import os
import aiohttp
from dotenv import load_dotenv

env_file = "./api/.env.local"
if not os.path.exists(env_file):
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


async def get_new_image(word):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            UNSPLASH_URL,
            headers={
                "Accept-Version": "v1",
                "Authorization": f"Client-ID {UNSPLASH_KEY}",
            },
            params={"query": word},
            timeout=10,
        )
        json = await response.json()
        return json
