#!/usr/bin/python3
""" for blueprint """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/status", strict_slashes=False, methods=['GET'])
def status():
    """ return the status of api """
    return jsonify(status="OK")


@app_views.route("/stats", strict_slashes=False, methods=['GET'])
def stats():
    """ return count of obj in storage"""
    count_State = storage.count(State)
    count_City = storage.count(City)
    count_Amenity = storage.count(Amenity)
    count_Place = storage.count(Place)
    count_Review = storage.count(Review)
    count_User = storage.count(User)
    return {
        "amenities": count_Amenity,
        "cities": count_City,
        "places": count_Place,
        "reviews": count_Review,
        "states": count_State,
        "users": count_User}
