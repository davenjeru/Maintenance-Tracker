from flask import Flask

from MaintenanceTrackerAPI.api.v1 import api_v1_blueprint
from MaintenanceTrackerAPI.api.v1.auth.login import jwt
from MaintenanceTrackerAPI.api.v1.database import Database
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

    if config_name == 'development':
        def prepare_tables():
            db = Database()
            db.drop_all()
            db.create_all()

        app.before_first_request(prepare_tables)

    @jwt.token_in_blacklist_loader
    def token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        db = Database()
        token = db.get_token_by_jti(jti)
        return bool(token)

    @jwt.user_loader_callback_loader
    def load_user(identity):
        db = Database()
        user = db.get_user_by_email(identity['email'])
        return user

    return app
