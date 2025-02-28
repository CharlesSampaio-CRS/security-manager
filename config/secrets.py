import base64
import json
import boto3

def get_secret():
    secret_name = "api-sec-manager"
    region_name = "us-east-1"

    client = boto3.client("secretsmanager", region_name=region_name)
    response = client.get_secret_value(SecretId=secret_name)

    secret_data = response["SecretString"]

    try:
        secret_dict = json.loads(secret_data)
        secret_key = secret_dict.get("JWT_SECRET_KEY", secret_data)
    except json.JSONDecodeError:
        secret_key = secret_data  
    try:
        return base64.b64decode(secret_key).decode()
    except Exception:
        return secret_key
