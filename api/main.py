from flask import Flask

if __name__ == "__main__":
  app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello world!"