from utils import helpers

class User:
    def __init__(self, email, password, role):
        self.email = email
        self.password = password
        self.role = role
        self.username = helpers.Helpers.generate_username(email)

