from flask import Flask

from MaintenanceTrackerAPI.api.v1 import api_v1_blueprint
from instance.config import app_config


# create app
def create_app(config_name):
    # initiate app
    app = Flask(__name__, instance_relative_config=True)

    # configurations
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # register blueprints
    app.register_blueprint(api_v1_blueprint)

    # register extensions
    return app
