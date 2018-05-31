from flask import Blueprint
from flask_restplus import Api

from .auth import auth_ns
from .users import users_ns

# initiate blueprint
api_v1_blueprint = Blueprint('apiV1', __name__, url_prefix='/api/v1')

# initiate api and its properties
api_v1 = Api(api_v1_blueprint)
api_v1.title = 'MAINTENANCE TRACKER API'
api_v1.description = 'To be consumed by the Maintenance Tracker front-end app'

# delete the default namespace
del api_v1.namespaces[0]

# api configurations
api_v1.catch_all_404s = True

# register namespaces related to this api
api_v1.add_namespace(auth_ns)
api_v1.add_namespace(users_ns)

# register extensions
