#!/usr/bin/python3
""" this file for state object """
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage
from flask import abort, request, jsonify, make_response


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['GET'])
def citiies_from_states(state_id):
    """ retrive cities from state_id"""
    obj = storage.get(State, state_id)
    if (obj is None):
        abort(404)
    list_cities = obj.cities
    list_dict_cities = []
    for city in list_cities:
        list_dict_cities.append(city.to_dict())

    return (jsonify(list_dict_cities))


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def city_with_city_id(city_id):
    """retrive city with city_id"""
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    city_dic = obj.to_dict()
    return (jsonify(city_dic))


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """ delete city_id """
    obj = storage.get(City, city_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states/<state_id>/cities", strict_slashes=False,
                 methods=['POST'])
def add_new_city(state_id):
    """ add new city"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    if 'name' not in request.get_json():
        abort(400, "Missing name")
    data = request.get_json(force=True, silent=True)
    new_city = City(**data)
    new_city.state_id = obj.id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ update city"""
    obj = storage.get(City, city_id)
    key_igonre = ['state_id', 'id', 'updated_at', 'created_at']
    if obj is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    json_data = request.get_json()

    for k, v in json_data.items():
        if k not in key_igonre:
            setattr(obj, k, v)

    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
