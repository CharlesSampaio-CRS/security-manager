from flask import Blueprint, request
from services.auth_service import AuthService

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/register', methods=['POST'])
def register():
    return AuthService.register(request.json)

@auth_routes.route('/login', methods=['POST'])
def login():
    return AuthService.login(request.json)
