#!/usr/bin/python3
""" this file for Amenity object """
from models.user import User
from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify


@app_views.route("users", strict_slashes=False,
                 methods=['GET'])
@app_views.route("users/<user_id>", strict_slashes=False,
                 methods=['GET'])
def user(user_id=None):
    """ list users with user_id"""
    list_of_user = []
    if (user_id):
        dic = storage.get(User, user_id)
        if dic is None:
            abort(404)
        return dic.to_dict()
    else:
        dic = storage.all(User).values()
        for v in dic:
            list_of_user.append(v.to_dict())
        return jsonify(list_of_user)


@app_views.route("users/<user_id>", strict_slashes=False,
                 methods=['DELETE'])
def user_delete(user_id):
    """ delete user with it's id"""
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("users", strict_slashes=False,
                 methods=['POST'])
def add_user():
    """ add new users"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if 'email' not in data:
        abort(400, "Missing email")
    if 'password' not in data:
        abort(400, "Missing password")
    obj = User(**data)
    obj.save()
    return (jsonify(obj.to_dict()), 201)


@app_views.route("users/<user_id>", strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """ update user """
    key_igonre = ['email', 'id', 'updated_at', 'created_at']

    obj = storage.get(User, user_id)
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
