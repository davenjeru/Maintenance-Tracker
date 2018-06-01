from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.users.single_user_all_requests \
    import SingleUserAllRequests, request_model
from MaintenanceTrackerAPI.api.v1.users.single_user_single_request \
    import SingleUserSingleRequest

users_ns = Namespace('users', description='Operations related to users')

users_ns.add_resource(SingleUserAllRequests,
                      '/<int:user_id>/requests',
                      endpoint='auth_single_user_all_requests')
users_ns.add_model('request_model', request_model)

users_ns.add_resource(SingleUserSingleRequest,
                      '/<int:user_id>/requests/<int:request_id>',
                      endpoint='users_single_user_single_request')
