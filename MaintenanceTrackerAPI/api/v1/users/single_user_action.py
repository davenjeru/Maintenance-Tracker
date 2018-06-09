from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class SingleUserAction(Resource):

    def post(self, user_id: int):
        pass
