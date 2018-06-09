from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.auth.login import Login, user_login_model
from MaintenanceTrackerAPI.api.v1.auth.logout import Logout
from MaintenanceTrackerAPI.api.v1.auth.signup import Register, \
    user_registration_model

# this is where the namespace, which holds related resources, is instantiated
auth_ns = Namespace('auth', description='Operations related to authentication')

auth_ns.add_resource(Register, '/signup', endpoint='auth_register')
auth_ns.add_model('user_registration_model', user_registration_model)

auth_ns.add_resource(Login, '/login', endpoint='auth_login')
auth_ns.add_model('user_login_model', user_login_model)

auth_ns.add_resource(Logout, '/logout', endpoint='auth_logout')
