#!/usr/bin/python3
""" for blueprint """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", strict_slashes=False, methods=['GET'])
def status():
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False, methods=['GET'])
def stats():
    return jsonify(storage.count())
