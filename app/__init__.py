from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config.Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
