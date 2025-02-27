from flask import jsonify
import bcrypt
from utils import helpers, jwt_util
from config import database

class AuthService:
    @staticmethod
    def validate_register_data(data):
        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        if not email or not password or not role:
            return {"error": "Please fill all fields (email, password, role)"}, 400

        if role not in ['admin', 'user']:
            return {"error": "The 'role' field must be 'admin' or 'user'"}, 400

        if database.users_collection.find_one({"email": email}):
            return {"error": "Email already registered"}, 409

        return None, None

    @staticmethod
    def register(data):
        validation_error, status_code = AuthService.validate_register_data(data)
        if validation_error:
            return jsonify(validation_error), status_code

        email = data.get('email')
        password = data.get('password')
        role = data.get('role')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        username = helpers.generate_username(email)

        user = {"email": email, "password": hashed_password, "role": role, "username": username}
        result = database.users_collection.insert_one(user)

        return jsonify({
            "message": "User successfully registered",
            "user_id": str(result.inserted_id),
            "username": username
        }), 201

    @staticmethod
    def validate_login_data(data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"error": "Please fill all fields (email and password)"}, 400

        return None, None

    @staticmethod
    def login(data):
        validation_error, status_code = AuthService.validate_login_data(data)
        if validation_error:
            return jsonify(validation_error), status_code

        email = data.get('email')
        password = data.get('password')

        user = database.users_collection.find_one({"email": email})
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return jsonify({"error": "Invalid credentials"}), 401

        token = jwt_util.generate_token(user.get("username"), user.get("email"), user.get("role"))

        return jsonify({"message": "Login successful", "token": token})
