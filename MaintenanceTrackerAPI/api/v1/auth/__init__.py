from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.auth.login import Login
from MaintenanceTrackerAPI.api.v1.auth.register import Register, user_registration_model

auth_ns = Namespace('auth', description='Operations related to authentication')

auth_ns.add_resource(Register, '/register', endpoint='auth_register')
auth_ns.add_model('user_registration_model', user_registration_model)

auth_ns.add_resource(Login, '/login', endpoint='auth_login')
