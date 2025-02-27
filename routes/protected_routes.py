from flask import Blueprint, jsonify, request
from middlewares.auth_middleware import AuthMiddleware

protected_bp = Blueprint('protected', __name__)

@protected_bp.route('/protected', methods=['GET'])
@AuthMiddleware.token_required
def protected():
    return jsonify({
        "message": f"Access granted for user {request.user_email} with role {request.role}"
    })
