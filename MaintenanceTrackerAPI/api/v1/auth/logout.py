from flask_login import current_user, logout_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.boilerplate import generate_auth_output

auth_ns = Namespace('auth')


class Logout(Resource):
    @auth_ns.response(200, 'user logged out successfully')
    @auth_ns.response(400, 'bad request')
    def post(self):
        """
        User Logout

        Makes use of Flask-Login

        If there is a user in session, they will be logged out,
         otherwise, 400 error is returned.
        In both cases the session cookie is cleared

        """
        try:
            output = generate_auth_output(self, current_user)
            logout_user()
            return self.api.make_response(output, 200)
        except AttributeError:
            logout_user()
            auth_ns.abort(400, 'no user in session')
