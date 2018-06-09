from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class SingleUser(Resource):
    def get(self, user_id):
        pass
