from flask import jsonify
import bcrypt
from utils import helpers, jwt_util
from config import database

class AuthService:
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
