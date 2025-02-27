from flask import jsonify, request
from jwt import ExpiredSignatureError, InvalidTokenError
from utils import jwt_util
from functools import wraps
from flask import request, jsonify
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

class AuthMiddleware:
    @staticmethod
    def token_required(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({"error": "Token missing"}), 401

            try:
                token = token.split(" ")[1]
                decoded = jwt_util.decode_token(token)
                request.user_email = decoded['sub']
                request.role = decoded['role']
            except ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 401
            except InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 401

            return f(*args, **kwargs)
        return decorated
