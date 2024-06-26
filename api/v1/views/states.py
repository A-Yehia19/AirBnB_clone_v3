#!/usr/bin/python3
"""states module"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from flasgger import swag_from
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'])
@swag_from('swagger_yaml/states_no_id.yml', methods=['GET', 'POST'])
def states_no_id():
    """states route without id"""
    if request.method == 'GET':
        all_states = storage.all('State')
        all_states = list(obj.to_json() for obj in all_states.values())
        return (jsonify(all_states))

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')

        if req_json.get("name") is None:
            abort(400, 'Missing name')

        new_object = State(**req_json)
        new_object.save()
        return (jsonify(new_object.to_json()), 201)


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/states_id.yml', methods=['PUT', 'GET', 'DELETE'])
def states_with_id(state_id=None):
    """states route with id"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return (jsonify(state_obj.to_json()))

    if request.method == 'DELETE':
        state_obj.delete()
        del state_obj
        return (jsonify({}))

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        state_obj.bm_update(req_json)
        return (jsonify(state_obj.to_json()))
