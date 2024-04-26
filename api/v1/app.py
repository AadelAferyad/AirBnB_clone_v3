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


if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    if HBNB_API_HOST is None:
        HBNB_API_HOST = "0.0.0.0"
    if HBNB_API_PORT is None:
        HBNB_API_PORT = 5000
    app.run(host=HBNB_API_HOST, threaded=True)
