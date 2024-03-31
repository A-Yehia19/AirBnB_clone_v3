#!/usr/bin/python3
"""index module"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """status route that returns the status of the API"""
    if request.method == 'GET':
        response = {"status": "OK"}
        return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def stats():
    """return count of all class objects"""
    if request.method == 'GET':
        response = {}
        PLURALS = {
            "User": "users",
            "City": "cities",
            "Place": "places",
            "State": "states",
            "Review": "reviews",
            "Amenity": "amenities"
        }
        for key, value in PLURALS.items():
            response[value] = storage.count(key)
        return jsonify(response)
