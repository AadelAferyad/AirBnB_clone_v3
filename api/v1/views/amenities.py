#!/usr/bin/python3
""" this file for Amenity object """
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify


@app_views.route("amenities", strict_slashes=False,
                 methods=['GET'])
@app_views.route("amenities/<amenity_id>", strict_slashes=False,
                 methods=['GET'])
def amenities(amenity_id=None):
    """ list Amenity with amenity_id"""
    list_of_amentity = []
    if (amenity_id):
        dic = storage.get(Amenity, amenity_id)
        if dic is None:
            abort(404)
        return dic.to_dict()
    else:
        dic = storage.all(Amenity).values()
        for v in dic:
            list_of_amentity.append(v.to_dict())
        return jsonify(list_of_amentity)


@app_views.route("amenities/<amenity_id>", strict_slashes=False,
                 methods=['DELETE'])
def amenity_delete(amenity_id):
    """ delete amenity with it's id"""
    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("amenities", strict_slashes=False,
                 methods=['POST'])
def add_amenity():
    """ add new amenities"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    obj = Amenity(**data)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route("amenities/<amenity_id>", strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    """ update amenity """
    key_igonre = ['state_id', 'id', 'updated_at', 'created_at']

    obj = storage.get(Amenity, amenity_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")

    for k, v in data.items():
        if k not in key_igonre:
            setattr(obj, k, v)
    obj.save()
    return jsonify(obj.to_dict()), 200
