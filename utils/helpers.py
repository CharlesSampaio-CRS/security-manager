import datetime


def generate_username(email: str) -> str:
    base_name = email.split("@")[0]
    date_suffix = datetime.datetime.now().strftime("%Y%m")
    return f"{base_name}_{date_suffix}"