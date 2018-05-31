from flask_login import login_required
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class SingleUserAllRequests(Resource):

    def get(self, user_id: int):
        pass

    @login_required
    @users_ns.response(201, 'Request made successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def post(self, user_id: int):
        """
        Make a request

        1. User must be logged in to make a request
        2. Your title should have between 10 and 70 characters
        3. Your body should have between 40 and 250 characters
        4. Duplicate requests will not be created

        """
        pass
