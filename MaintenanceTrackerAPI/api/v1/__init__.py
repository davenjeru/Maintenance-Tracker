from flask import Blueprint
from flask_restplus import Api

from MaintenanceTrackerAPI.api.v1.auth.login import jwt
from MaintenanceTrackerAPI.api.v1.requests import requests_ns
from .auth import auth_ns
from .users import users_ns

# initiate blueprint
api_v1_blueprint = Blueprint('apiV1', __name__, url_prefix='/api/v1')

# initiate api and its properties

authorizations = dict(
    access_token={
        'type': 'apiKey',
        'in': 'header',
        'name': 'ACCESS_TOKEN'
    }
)

api_v1 = Api(api_v1_blueprint)
api_v1.title = 'MAINTENANCE TRACKER API'
api_v1.description = 'To be consumed by the Maintenance Tracker front-end app'
api_v1.authorizations = authorizations

# delete the default namespace
del api_v1.namespaces[0]

# api configurations
api_v1.catch_all_404s = True

# register namespaces related to this api
api_v1.add_namespace(auth_ns)
api_v1.add_namespace(users_ns)
api_v1.add_namespace(requests_ns)

# register extensions
jwt._set_error_handler_callbacks(api_v1)
