from flask import Flask
from routes.auth_routes import auth_routes
from routes.protected_routes import protected_bp

from config.secrets import get_secret

app = Flask(__name__)
app.config['SECRET_KEY'] = get_secret()

app.register_blueprint(auth_routes, url_prefix='/auth')
app.register_blueprint(protected_bp, url_prefix='/protected')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
