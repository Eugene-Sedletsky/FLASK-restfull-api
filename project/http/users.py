""" Users entity RESTfull controller handling JSON requests/responses """

import os
import json
import jsonschema


from flask import Blueprint, jsonify, current_app, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from project import db
from project.models.user import User
from project.exceptions.UserConsentRevoked import UserConsentRevoked

controller_blueprint = Blueprint('user_resources', __name__)

# Get the current script's directory path
current_directory = os.path.dirname(os.path.abspath(__file__))


@controller_blueprint.route('/users', methods=['GET'])
def get_user_collection():
    """ Handle GET request to get user entity collection """

    current_app.logger.info('Fetching user collection from the database.')

    # Query the database to get the collection of MyModule objects
    user_collection = User.query.all()

    # Convert the collection of MyModule objects into a list of dictionaries
    my_module_list = [
        {'id': item.id, 'name': item.name, 'email': item.email}
        for item in user_collection
    ]

    # Return the list of dictionaries as a JSON response
    return jsonify(my_module_list)


@controller_blueprint.route('/users', methods=['POST'])
def create_user():
    """ Handle POST request to create a new user entity """

    # Get the data from the POST request JSON payload
    data = request.get_json()

    # Construct the full path to user_schema.json
    schema_file_path = os.path.join(current_directory, 'user_create_schema.json')

    # Load the JSON Schema from the file
    with open(schema_file_path, mode='r', encoding='utf-8') as schema_file:
        user_create_schema = json.load(schema_file)

    # Validate the data against the JSON Schema
    try:
        jsonschema.validate(data, user_create_schema)
    except jsonschema.ValidationError as exception:
        # Provide a custom user-friendly error message
        error_message = f"Invalid data received. {str(exception)}"

        return jsonify({'error': error_message}), 400

    try:
        new_user = User(
            email=data.get("email", None),
            password=data.get("password", None),
            consent=data.get("consent", None),
            name=data.get("name", None)
        )

        new_user.remember_token = data.get("remember_token", None)
        new_user.memo = data.get("memo", None)

        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info('User entity created successfully.')

        return jsonify(new_user.to_dict()), 201

    except IntegrityError as exception:
        db.session.rollback()
        current_app.logger.error(f'Error creating User entity: {type(exception)}')

        return jsonify({'error': 'Error creating User entity.'}), 400


@controller_blueprint.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id : int):
    """ Handle GET request to get already existing user entity """
    try:
        user = User.query.filter_by(_id=user_id).one()

        return jsonify(user.to_dict()), 200

    except NoResultFound:

        return jsonify({'error': f'User not found: id: {user_id}'}), 404


@controller_blueprint.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id : int):
    """ Handle DELETE request to delete already existing user entity """

    try:
        user = User.query.filter_by(_id=user_id).one()
         # Delete the user from the database
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message' : f'User {user_id} deleted'}), 202

    except NoResultFound:

        return jsonify({'error': f'User not found: id: {id}'}), 404

    except Exception as exception: # pylint: disable=broad-except
        #@ToDo - find ways to test this exception
        current_app.logger.error(f'Error while User deleting : {str(exception)}')

        db.session.rollback()

        return jsonify({'error': f'Error occurred while deleting user: {id}'}), 400


@controller_blueprint.route('/users/<int:user_id>', methods=['PUT', 'PATCH'])
def update_user(user_id : int):
    """ Handle PUT/PATH request to amend already existing user entity """

    # Get the data from the POST request JSON payload
    data = request.get_json()

    current_app.logger.error(f'Data received: {data}')


    # Construct the full path to user_schema.json
    schema_file_path = os.path.join(current_directory, 'user_update_schema.json')

    # Load the JSON Schema from the file
    with open(schema_file_path, mode='r', encoding='utf-8') as schema_file:
        user_create_schema = json.load(schema_file)

    # Validate the data against the JSON Schema
    try:
        jsonschema.validate(data, user_create_schema)
    except jsonschema.ValidationError as exception:
        # Provide a custom user-friendly error message
        error_message = f"Invalid data was received {str(exception)}"
        current_app.logger.error(f'Error while User updating: {error_message}')

        return jsonify({'error': error_message}), 400

    try:
        user = User.query.filter_by(_id=user_id).one()

        user.password = data.get("password", user.password)
        user.remember_token = data.get("remember_token", user.remember_token)
        user.email = data.get("email", user.email)
        user.name = data.get("name", user.name)
        user.memo = data.get("memo", user.memo)
        user.consent = data.get("consent", user.consent) # this should trigger deletion

        if data.get("email_confirmed", None) is True:
            user.set_email_verified()

        db.session.commit()

        return jsonify(user.to_dict()), 200

    except UserConsentRevoked:

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message' : f'User {user_id} deleted'}), 202

    except NoResultFound:

        return jsonify({'error': f'User not found: id: {user_id}'}), 404

    except Exception as exception: # pylint: disable=broad-except
        # @ToDo find a way to test this while functional testing
        db.session.rollback()
        current_app.logger.error(f'Error while User updating : {str(exception)}')

        return jsonify({'error': "Something went wrong"}), 400
