import mongomock
import pytest
from flask import Flask
from unittest.mock import patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.database import users_collection
from services.auth_service import AuthService
from routes.auth_routes import auth_routes  

@pytest.fixture
def app():
    """Configuração do Flask para os testes."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(auth_routes, url_prefix='/auth')  
    return app

@pytest.fixture
def client(app):
    """Cliente de teste do Flask."""
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_database():
    """Reseta o banco de dados antes de cada teste."""
    with patch('config.database.users_collection', mongomock.MongoClient().db.users):
        yield

@patch('services.auth_service.database.users_collection.find_one')
@patch('services.auth_service.bcrypt.checkpw')
@patch('services.auth_service.jwt_util.generate_token')
def test_login_success(mock_generate_token, mock_checkpw, mock_find_one, client):
    mock_find_one.return_value = {
        "email": "test@example.com",
        "password": b"hashedpassword",
        "role": "user"
    }
    mock_checkpw.return_value = True
    mock_generate_token.return_value = "jwt_token_example"

    data = {'email': 'test@example.com', 'password': 'password123'}
    response = client.post('/auth/login', json=data)  
    assert response.status_code == 200
    response_data = response.get_json()
    assert response_data["message"] == "Login successful"
    assert "token" in response_data

@patch('services.auth_service.database.users_collection.find_one')
def test_login_invalid_credentials(mock_find_one, client):
    mock_find_one.return_value = None
    data = {'email': 'test@example.com', 'password': 'wrongpassword'}
    response = client.post('/auth/login', json=data)  
    assert response.status_code == 401
    response_data = response.get_json()
    assert response_data['error'] == "Invalid credentials"
