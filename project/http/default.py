""" Root/Default get response controller """

from flask import Blueprint, jsonify

controller_blueprint = Blueprint('default_resources', __name__)

@controller_blueprint.route('/')
def check_status():
    """ If app is stable enough to get there, will return status: OK"""
    return jsonify({'status': 'ok'})
