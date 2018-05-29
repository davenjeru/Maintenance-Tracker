from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.users.users_all_requests import UsersAllRequests
from MaintenanceTrackerAPI.api.v1.users.users_single_request import UsersSingleRequests

# initiate the namespace
users_ns = Namespace('users', description='Operations related to users')

# add resources related to this namespace and the models in those resource
users_ns.add_resource(UsersAllRequests, '/requests')
users_ns.add_resource(UsersSingleRequests, '/requests/<int:request_id>')
