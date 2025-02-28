from datetime import datetime, timedelta
import jwt
from typing import Dict

from config.secrets import get_secret

def generate_token(username: str, email: str, role: str) -> str:
    """Gera um JWT válido por 1 hora com HS512."""
    expiration_time = 2 * 3600
    grants = get_grants(role) 

    payload = {
        'sub': username,
        'email': email,
        'grants': grants,
        'authorities': grants,
        'credentials': role,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=expiration_time)
    }

    secret_key = get_secret()
    token = jwt.encode(payload, secret_key, algorithm="HS512")
    return token

def decode_token(token: str) -> Dict:
    """Decodifica um token JWT e retorna os dados."""
    secret_key = get_secret()
    return jwt.decode(token, secret_key, algorithms=["HS512"])

def get_grants(role: str):
    """Retorna permissões baseadas no papel do usuário."""
    if role.upper() == "ADMIN":
        return ["ROLE_ADMIN", "ROLE_USER"]
    return ["ROLE_USER"]


