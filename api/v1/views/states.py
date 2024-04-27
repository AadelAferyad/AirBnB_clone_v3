#!/usr/bin/python3
""" this file for state object """
from models.state import State
from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify

st = State()
st.to_dict()


@app_views.route("states", strict_slashes=False,
                 methods=['GET'])
@app_views.route("states/<state_id>", strict_slashes=False,
                 methods=['GET'])
def state(state_id=None):
    """ list state with state id"""
    list_of_states = []
    if (state_id):
        dic = storage.get(State, state_id)
        if dic is None:
            abort(404)
        return dic.to_dict()
    else:
        dic = storage.all().values()
        for v in dic:
            list_of_states.append(v.to_dict())
        return jsonify(list_of_states)


@app_views.route("states/<state_id>", strict_slashes=False,
                 methods=['DELETE'])
def state_delete(state_id):
    """ delete state with it's id"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return (jsonify({}), 200)


@app_views.route("states", strict_slashes=False,
                 methods=['POST'])
def add_state():
    """ add new state"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    new_s = State(**data)
    new_s.save()
    return (jsonify(new_s.to_dict()), 201)


@app_views.route("states/<state_id>", strict_slashes=False,
                 methods=['PUT'])
def update_state(state_id):
    """ ipdate state """
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    obj.name = data.get("name", obj.name)
    obj.save()
    return jsonify(obj.to_dict()), 200
