from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import os


db = SQLAlchemy()


def init_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    load_dotenv()
    db_url = os.environ.get('SQLALCHEMY_DATABASE_URI')

    with app.app_context():
        from . import routes
        from . import models

        db.init_app(app)

        db.create_all()

        return app