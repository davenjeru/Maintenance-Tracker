from flask_login import login_required
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class SingleUserAllRequests(Resource):

    def get(self, user_id: int):
        pass

    @login_required
    @users_ns.response(201, 'Post created successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def post(self, user_id: int):
        """
        Add a post

        1. User must be logged in to create a post
        2. Your title should have between 10 and 70 characters
        3. Your body should have between 40 and 500 characters
        4. Duplicate posts will not be created

        """
        pass
