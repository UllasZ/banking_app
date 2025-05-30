# app.py

from flask import Flask
from src.banking_app.config import Config
from src.banking_app.apis.auth import auth_bp
from src.banking_app.apis.users import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(users_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/')

    @app.route('/')
    def hello():
        return 'Hello, Welcome to XYZ Bank!'

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=False)


# Docker
# accounts, transactions, sessions.