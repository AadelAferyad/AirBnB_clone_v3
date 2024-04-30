#!/usr/bin/python3
""" this file for Amenity object """
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify


@app_views.route("cities/<city_id>/places", strict_slashes=False,
                 methods=['GET'])
def places(city_id=None):
    """ list places with city_id"""
    list_of_places = []
    if (city_id):
        dic = storage.get(City, city_id)
        if dic is None:
            abort(404)
        dic = storage.all(Place).values()
        for v in dic:
            if v.city_id == city_id:
                list_of_places.append(v.to_dict())

        return jsonify(list_of_places)


@app_views.route("places/<place_id>", strict_slashes=False,
                 methods=['GET'])
def places_with_id(place_id=None):
    """ list places with place_id"""
    if place_id:
        dic = storage.get(Place, place_id)
        if dic is None:
            abort(404)
        return dic.to_dict()


@app_views.route("places/<place_id>", strict_slashes=False,
                 methods=['DELETE'])
def place_delete(place_id):
    """ delete place with it's id"""
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("cities/<city_id>/places", strict_slashes=False,
                 methods=['POST'])
def add_place(city_id):
    """ add new place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data.get('user_id'))
    print(user)
    print(data.get('user_id'))
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")
    obj = Place(**data)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route("places/<place_id>", strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    """ update place """
    key_ig = ['user_id', 'id', 'city_id', 'updated_at', 'created_at']

    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")

    for k, v in data.items():
        if k not in key_ig:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
