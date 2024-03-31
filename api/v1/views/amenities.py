#!/usr/bin/python3
"""amniety module"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.amenity import Amenity
from flasgger.utils import swag_from


@app_views.route('/amenities/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/amenities_no_id.yml', methods=['GET', 'POST'])
def amenities_no_id(amenity_id=None):
    """amenities route without id"""
    if request.method == 'GET':
        all_amenities = storage.all('Amenity')
        all_amenities = [obj.to_json() for obj in all_amenities.values()]
        return (jsonify(all_amenities))

    if request.method == 'POST':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')

        if request_json.get('name') is None:
            abort(400, 'Missing name')

        new_amenity = Amenity(**request_json)
        new_amenity.save()
        return (jsonify(new_amenity.to_json()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/amenities_id.yml', methods=['GET', 'DELETE', 'PUT'])
def amenities_with_id(amenity_id=None):
    """amenities route with id"""
    amenity_obj = storage.get('Amenity', amenity_id)
    if amenity_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return (jsonify(amenity_obj.to_json()))

    if request.method == 'DELETE':
        amenity_obj.delete()
        del amenity_obj
        return (jsonify({}), 200)

    if request.method == 'PUT':
        request_json = request.get_json()
        if request_json is None:
            abort(400, 'Not a JSON')
        amenity_obj.bm_update(request_json)
        return (jsonify(amenity_obj.to_json()), 200)
