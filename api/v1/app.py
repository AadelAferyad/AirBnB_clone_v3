#!/usr/bin/python3
""" this file is for my api """
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def close(ctx):
    """ called when the programm ends """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ not found """
    return {"error": "Not found"}


if __name__ == "__main__":

    if getenv("HBNB_API_HOST"):
        host = getenv("HBNB_API_HOST")
    else:
        host = "0.0.0.0"
    if getenv("HBNB_API_PORT"):
        port = int(getenv("HBNB_API_PORT"))
    else:
        port = 5000

    app.run(host=host, port=port, threaded=True)
