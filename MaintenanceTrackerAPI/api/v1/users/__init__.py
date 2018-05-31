from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.users.single_user_all_requests import SingleUserAllRequests

users_ns = Namespace('users', description='Operations related to users')

users_ns.add_resource(SingleUserAllRequests, '/<int:user_id>/requests', endpoint='auth_single_user_all_requests')
