from flask import Flask
from dotenv import load_dotenv
import os




def init_app():
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    load_dotenv()

    with app.app_context():
        from . import routes
        from . import models


        return app