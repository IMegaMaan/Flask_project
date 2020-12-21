from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import DevelopmentConfig


# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
# JSON-RPC, add to project https://pypi.org/project/Flask-JSONRPC/

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object(DevelopmentConfig)

    db.init_app(app)

    # Working with login
    login_manager = LoginManager()
    login_manager.login_view = 'authentication.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # authentication and main(storage) blueprints registration
    from .storage import storage
    from .authentication import authentication

    app.register_blueprint(authentication)
    app.register_blueprint(storage)

    return app
