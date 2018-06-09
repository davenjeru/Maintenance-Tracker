from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.users.all_users import AllUsers
from MaintenanceTrackerAPI.api.v1.users.single_user import SingleUser
from MaintenanceTrackerAPI.api.v1.users.single_user_action import \
    SingleUserAction
from MaintenanceTrackerAPI.api.v1.users.single_user_all_requests \
    import SingleUserAllRequests, request_model
from MaintenanceTrackerAPI.api.v1.users.single_user_single_request \
    import SingleUserSingleRequest

# this is where the namespace, which holds related resources, is instantiated
users_ns = Namespace('users', description='Operations related to users')

users_ns.add_resource(AllUsers, '/', endpoint='users')
users_ns.add_resource(SingleUser, '/<int:user_id>',
                      endpoint='users_single_user')

users_ns.add_resource(SingleUserAllRequests,
                      '/requests',
                      endpoint='users_single_user_all_requests')
users_ns.add_model('request_model', request_model)

users_ns.add_resource(SingleUserSingleRequest,
                      '/requests/<int:request_id>',
                      endpoint='users_single_user_single_request')

users_ns.add_resource(SingleUserAction,
                      '/<int:user_id>/<string:action>',
                      endpoint='users_single_user_action')
