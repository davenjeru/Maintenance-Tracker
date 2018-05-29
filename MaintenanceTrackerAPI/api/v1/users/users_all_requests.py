from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class UsersAllRequests(Resource):
    def get(self):
        pass

    def post(self):
        pass
