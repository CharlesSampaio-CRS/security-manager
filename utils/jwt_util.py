import datetime
from typing import Dict
import jwt
from config import secrets

def generate_token(user: Dict) -> str:
    payload = {
        "sub": user.get("email"),
        "role": user.get("role"),
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=3600)
    }
    return jwt.encode(payload, secrets.get_secret(), algorithm="HS256")

def decode_token(token: str) -> Dict:
    return jwt.decode(token, secrets.get_secret(), algorithms=["HS256"])
