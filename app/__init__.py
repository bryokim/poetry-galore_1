#!/usr/bin/python3

import os

from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(test_config=None):
    """Create a Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config("APP_SETTINGS"))
    if test_config is None:
        # load the instance config, if it exists, when not testing.
        # app.config.from_pyfile("config.py", silent=True)
        pass
    else:
        # Load the test config if passed in.
        app.config.from_mapping(test_config)

    # ensure the instance folder exists.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app.models.user import User

    login_manager.refresh_view = "accounts_view.login"
    login_manager.login_view = "accounts_view.login"
    login_manager.login_message = "Login required."
    login_manager.needs_refresh_message = (
        "Please refresh your session before continuing"
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # with app.before_request():
    #     app.config["storage"] = DBStorage(db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == user_id).first()

    from app.api.v1.views import accounts_view
    from app.api.v1.views import core_view

    app.register_blueprint(accounts_view)
    app.register_blueprint(core_view)
    app.add_url_rule("/", endpoint="accounts_view.home")

    return app
