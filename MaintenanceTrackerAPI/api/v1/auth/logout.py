from flask_restplus import Resource
from flask_restplus.namespace import Namespace

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
        pass
