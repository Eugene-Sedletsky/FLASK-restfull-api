"""
This file (test_api.py) contains the functional tests for the API functions
"""
import re


def test_default_status_response(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN response must be 200
    """

    response = test_client.get('/')
    assert response.status_code == 200


def test_get_user_empty_collection(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users' page is requested (GET) on fresh instance
    THEN must not have any users
    """

    response = test_client.get('/users')
    assert response.status_code == 200


def test_create_user_response_contain_user_fields(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users' page is requested by (POST) with data
    THEN must return new user data
    """

    data = {
        'name': 'John Doe2',
        'email': 'john.doe2@example.com',
        'consent' : True,
    }

    response = test_client.post('/users', json=data)

    assert response.is_json

    json_data = response.json

    assert response.status_code == 201
    assert 'name' in json_data
    assert 'email' in json_data
    assert 'consent' in json_data
    assert not 'password' in json_data
    assert 'email_verified_at' in json_data
    assert 'remember_token' in json_data
    assert 'memo' in json_data


def test_create_user_from_valid_data(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN adding a new user with valid data
    THEN response must return new user data
    """

    data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'consent' : True,
    }

    # Send the POST request with the data
    response = test_client.post('/users', json=data)

    assert response.is_json

    json_data = response.json

    assert response.status_code == 201

    assert 'name' in json_data
    assert 'email' in json_data
    assert 'consent' in json_data
    assert not 'password' in json_data
    assert 'email_verified_at' in json_data
    assert 'remember_token' in json_data
    assert 'memo' in json_data

    assert json_data['consent'] is True
    assert json_data['email_verified_at'] is None
    assert json_data['remember_token'] is None
    assert json_data['memo'] is None
    assert json_data['name'] == 'John Doe'
    assert json_data['email'] == 'john.doe@example.com'


def test_create_user_constraint_empty_name(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN adding a new user with valid data
    THEN response should return new user data
    """

    data = {
        'email': 'john.doe@example.com',
        'consent' : True,
    }

    response = test_client.post('/users', json=data)

    assert response.is_json
    assert response.status_code == 400


def test_create_user_constraint_empty_email(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN adding a new user without an email
    THEN response should return an error
    """

    data = {
        'name': 'John Doe',
        'consent' : True,
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 400
    assert response.is_json


def test_create_user_constraint_empty_consent(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN adding a new user without a consent property
    THEN response should return an error
    """

    data = {
        'email': 'john.doe@example.com',
        'name': 'John Doe',
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 400
    assert response.is_json


def test_create_user_constraint_without_consent(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN adding a new user without a consent
    THEN response should return an error
    """

    data = {
        'email': 'john.doe@example.com',
        'name': 'John Doe',
        'consent' : False,
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 400
    assert response.is_json


def test_create_user_with_existing_email_constrain(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN adding a two new users without same email
    THEN response should return an error
    """

    data = {
        'email': 'user1@example.com',
        'name': 'user1',
        'consent' : True,
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 201
    assert response.is_json

    response = test_client.post('/users', json=data)

    assert response.status_code == 400
    assert response.is_json


def test_get_created_user(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN adding a new users
    THEN we must able to retrieve this user by GET request,
         return data must be without a password field
    """

    data = {
        'email': 'user5@example.com',
        'name': 'user5',
        'consent' : True,
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 201
    assert response.is_json
    json_data = response.json

    response = test_client.get(f"/users/{json_data['id']}")
    assert response.status_code == 200
    assert response.is_json

    json_data = response.json

    assert 'name' in json_data
    assert 'email' in json_data
    assert 'consent' in json_data
    assert not 'password' in json_data
    assert 'email_verified_at' in json_data
    assert 'remember_token' in json_data
    assert 'memo' in json_data

    assert json_data['consent'] is True
    assert json_data['email_verified_at'] is None
    assert json_data['remember_token'] is None
    assert json_data['memo'] is None
    assert json_data['name'] == 'user5'
    assert json_data['email'] == 'user5@example.com'


def test_get_not_existing_user(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN we requesting data for non existing user
    THEN response should return an error 404
    """

    response = test_client.get("/users/100243435")

    assert response.status_code == 404
    assert response.is_json


def test_user_deletion(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN we added user and then we deleting this user
    THEN response for delete should be 202,
         consecutive deletion request must return an error 404
    """

    data = {
        'email': 'user4@example.com',
        'name': 'user4',
        'consent' : True,
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 201
    assert response.is_json
    json_data = response.json
    user_id = json_data['id']

    response = test_client.delete(f"/users/{user_id}")

    assert response.status_code == 202
    assert response.is_json

    response = test_client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.is_json


def test_deletion_not_existing_user(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN we requesting data deletion for non existing user
    THEN response must return an error 404
    """

    user_id = 99999
    response = test_client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.is_json



def test_user_create_with_unexpected_payload(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN we requesting user to be created and our request contain unexpected data, like ID
    THEN response must return an error 400
    """

    data = {
        'email': 'user10@example.com',
        'name': 'user10',
        'consent' : True,
        'id' : 100
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 400
    assert response.is_json


def test_update_user_by_unexpected_data(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN we requesting user to be updated and our request contain unexpected data, like ID
    THEN response must return an error 400
    """

    user_id = 99999
    data = {
        'id' : user_id
    }

    response = test_client.put(f"/users/{user_id}", json=data)

    assert response.status_code == 400
    assert response.is_json


def test_update_not_existing_user(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN we requesting non existing user to be updated
    THEN response must return an error 404
    """

    user_id = 99999
    data = {
        'email': 'update.email@example.com',
    }

    response = test_client.put(f"/users/{user_id}", json=data)

    assert response.status_code == 404
    assert response.is_json


def test_user_update_email(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN we requesting user email to be updated
    THEN response must return an error 200
    """

    data = {
        'email': 'user11@example.com',
        'name': 'user11',
        'consent' : True
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 201
    assert response.is_json

    json_data = response.json
    user_id = json_data['id']

    data = {
        'email': 'update.email@example.com',
    }

    response = test_client.put(f"/users/{user_id}", json=data)

    assert response.status_code == 200
    assert response.is_json


def test_user_verify_email(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN we creating user, email must be marked as not verified,
         with consecutive email confirmed update request
    THEN response must return an error 200, and email_verified_at must be set
    """

    data = {
        'email': 'user11@example.com',
        'name': 'user11',
        'consent' : True
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 201
    assert response.is_json

    json_data = response.json
    user_id = json_data['id']

    assert json_data['email_verified_at'] is None

    data = {
        'email_confirmed': True,
    }

    response = test_client.put(f"/users/{user_id}", json=data)

    assert response.status_code == 200
    assert response.is_json

    json_data = response.json

    assert not json_data['email_verified_at'] is None

    # Define the pattern using regular expressions
    pattern = r"^\w{3}, \d{2} \w{3} \d{4} \d{2}:\d{2}:\d{2} \w{3}$"

    # Check if the date string matches the pattern
    match = re.match(pattern, json_data['email_verified_at'])

    # Assert that the string matches the pattern
    assert match is not None, "Date string does not match the expected pattern."



def test_user_revoke_consent(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/users' page is requested by (POST) with data and consequentially user was revoking
         consent on existing record
    THEN User record should be deleted from the database, consecutive get request must fail with 404
    """

    data = {
        'email': 'user15@example.com',
        'name': 'user15',
        'consent' : True
    }

    response = test_client.post('/users', json=data)

    assert response.status_code == 201
    assert response.is_json

    json_data = response.json
    user_id = json_data['id']


    data = {
        'consent': False,
    }

    response = test_client.put(f"/users/{user_id}", json=data)

    assert response.status_code == 202
    assert response.is_json

    response = test_client.get(f"/users/{user_id}")

    assert response.status_code == 404
    assert response.is_json
