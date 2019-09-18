import pytest
import sys
from app import create_app, db
from app.models import Accommodation, User
from tests.config_test import TestConfig
from tests import test_data

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    
    # create the app with common test config
    app = create_app(TestConfig)
    test_data.insert_data(app)

    yield app

    # TEARDOWN PHASE
    test_data.cleanup(app)

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='test@test.com', password='test'):
        return self._client.post(
            '/api/login',
            data={'email': email, 'password': password}
        )
    # TODO: fix this.
    def logout(self):
        return self._client.get('/api/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)



