from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv(dotenv_path="./api/.env.local")

UNSPLASH_URL = "https://api.unsplash.com/photos/random"
UNSPLASH_KEY = os.environ.get("UNSPLASH_KEY", "")

if not UNSPLASH_KEY:
    raise EnvironmentError("Please provide UNSPLASH_KEY in .env.local file")

app = Flask(__name__)
CORS(app)


@app.route("/new-image")
def new_image():
    word = request.args.get("query")
    response = requests.get(
        UNSPLASH_URL,
        headers={"Accept-Version": "v1", "Authorization": f"Client-ID {UNSPLASH_KEY}"},
        params={"query": word},
    )

    data = response.json()
    return data


if __name__ == "__main__":
    app.run()
