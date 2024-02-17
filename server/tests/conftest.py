import pytest
from application import app as flask_app
from application import db
from flask import json
from application.utils.Validation import Validation

@pytest.fixture
def app():
    """
    Fixture for initializing the Flask app within a context.

    Yields:
        Flask app instance.
    """
    with flask_app.app_context():
        yield flask_app

@pytest.fixture
def client(app):
    """
    Fixture for creating a test client for the Flask app.

    Args:
        app: Initialized Flask app.

    Returns:
        Test client for the Flask app.
    """
    return app.test_client()

@pytest.fixture
def user1(client):
    """
    Fixture for creating a test user and logging in.

    Args:
        client: Test client for the Flask app.

    Returns:
        Dictionary containing user information.
    """
    user = {
        "email": "test@gmail.com",
        "name": "test1",
        "password": "Testingg1",
    }
    client.post(
        '/signup', 
        data=json.dumps(user), 
        content_type="application/json"
    )
    user = {
        "email": "test@gmail.com",
        "name": "test1",
        "password": "Testingg1",
        "remember_me": "True"
    }
    response = client.post(
        '/login',
        data=json.dumps(user),
        content_type="application/json"
    )
    return json.loads(response.data)

@pytest.fixture
def user2(client):
    """
    Fixture for creating a second test user and logging in.

    Args:
        client: Test client for the Flask app.

    Returns:
        Dictionary containing user information.
    """
    user = {
        "email": "test2@gmail.com",
        "name": "test2",
        "password": "Testingg1",
    }
    client.post(
        '/signup', 
        data=json.dumps(user), 
        content_type="application/json"
    )
    user = {
        "email": "test2@gmail.com",
        "name": "test2",
        "password": "Testingg1",
        "remember_me": "True"
    }
    response = client.post(
        '/login',
        data=json.dumps(user),
        content_type="application/json"
    )
    return json.loads(response.data)

@pytest.fixture
def validator():
    """
    Fixture for initializing the Validation object.

    Returns:
        Validation object.
    """
    return Validation()
