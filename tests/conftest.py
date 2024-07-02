""" Test instance fixture and test-flow definitions.
"""
import os
import sys
import pytest

# Assuming conftest.py is inside the tests directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# pylint: disable=wrong-import-position
from project import create_app, db # pylint: disable=import-error
from project.models.user import User # pylint: disable=import-error
# pylint: enable=wrong-import-position

# --------
# Fixtures
# --------

@pytest.fixture(scope='module')
def new_user():
    """ Prepare instance of a new User object"""

    user = User('test@example.com',  'password123', True)

    return user


@pytest.fixture(scope='module')
def test_client():
    """Prepare instance of Flask app for functional testings, with database
    cleanup and applying test environment settings to Flask app.
    """

    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!

            db.session.remove()
            db.drop_all()


@pytest.fixture(scope='module')
def cli_test_client():
    """Prepare instance of Flask app for functional cli testings,
    and applying test environment settings to Flask app.
    """
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    runner = flask_app.test_cli_runner()

    yield runner  # this is where the testing happens!
