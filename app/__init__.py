from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import DevelopmentConfig
import os

# connect to Database
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)
    db.init_app(app)

    # Working with login
    # see documentation Flask-Login
    login_manager = LoginManager()
    login_manager.session_protection = 'basic'
    login_manager.login_view = 'authentication.login'
    login_manager.init_app(app)

    # to avoid circular import of components placed inside function
    from .models import User
    # see documentation Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # authentication and main(storage) blueprints registration
    # to avoid circular import of components placed inside function
    from .storage import storage
    from .authentication import authentication

    app.register_blueprint(authentication)
    app.register_blueprint(storage)

    return app
