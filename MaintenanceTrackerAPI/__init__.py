import os

from flask import Flask
from flask_cors import CORS

from MaintenanceTrackerAPI.api.v1 import api_v1_blueprint
from MaintenanceTrackerAPI.api.v1.auth.login import jwt
from MaintenanceTrackerAPI.api.v1.database import db
from MaintenanceTrackerAPI.api.v1.exceptions import UserTransactionError
from MaintenanceTrackerAPI.api.v1.models.user_model import User
from instance.config import app_config


# create app
def create_app(config_name):
    """
    Class for creating the flask app using different configurations
    :param config_name:
    :return: The created flask app
    :rtype: Flask
    """
    # initiate app
    app = Flask(__name__, instance_relative_config=True)

    # configurations
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # register blueprints
    app.register_blueprint(api_v1_blueprint)

    # register extensions
    jwt.init_app(app)
    CORS(app)

    def prepare_tables():
        if config_name == 'development':
            db.drop_all()
            db.create_all()
        if config_name == 'production':
            db.create_all()

        # create default administrator account
        try:
            User(os.getenv('ADMIN_EMAIL'), os.getenv('ADMIN_PASSWORD'),
                 os.getenv('ADMIN_QUESTION'), os.getenv('ADMIN_ANSWER'),
                 'Administrator')
        except UserTransactionError:
            pass

    app.before_first_request(prepare_tables)

    @jwt.token_in_blacklist_loader
    def token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        token = db.get_token_by_jti(jti)
        return bool(token)

    @jwt.user_loader_callback_loader
    def load_user(identity):
        user = db.get_user_by_email(identity['email'])
        return user

    return app
