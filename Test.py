import pytest
import json
from project import create_jwt, JWKSHandler # Assuming you refactor your code to use Flask and save it in 'your_server_module.py'

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_jwk(client):
    response = client.get('/.well-known/jwk.json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'kty' in data
    assert 'kid' in data
    assert 'n' in data
    assert 'e' in data

def test_auth(client):
    response = client.post('/auth')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data

def test_unsupported_methods(client):
    unsupported_methods = ['put', 'delete', 'patch', 'head']
    for method in unsupported_methods:
        response = getattr(client, method)('/auth')
        assert response.status_code == 405  # Method Not Allowed
