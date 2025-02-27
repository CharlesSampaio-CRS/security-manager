import datetime
from typing import Dict
import jwt
from config import secrets


def generate_token(username, email, role):
    expiration_time = 3600  
    payload = {
        'sub': username,
        'email': email,
        'grants': get_grants(role),
        'authorities': get_grants(role),
        'credentials': role,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_time)
    }

    token = jwt.encode(payload, secrets.get_secret(), algorithm='HS256')
    return token

def decode_token(token: str) -> Dict:
    return jwt.decode(token, secrets.get_secret(), algorithms=["HS256"])

def get_grants(role):
    if role.upper() == "ADMIN":
        return ["ROLE_ADMIN", "ROLE_USER"]
    return ["ROLE_USER"]


