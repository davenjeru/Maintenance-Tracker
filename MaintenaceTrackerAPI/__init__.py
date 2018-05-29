from flask import Flask

from MaintenaceTrackerAPI.api.v1 import api_v1_blueprint

# initiate app
app = Flask(__name__)

# configurations

# register blueprints
app.register_blueprint(api_v1_blueprint)

# register extensions
