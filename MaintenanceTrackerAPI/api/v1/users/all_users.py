from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class AllUsers(Resource):
    def get(self):
        pass
