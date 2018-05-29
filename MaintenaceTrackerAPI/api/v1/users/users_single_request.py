from flask_restplus import Resource
from flask_restplus.namespace import Namespace

users_ns = Namespace('users')


class UsersSingleRequests(Resource):
    def get(self, request_id: int):
        pass

    def put(self, request_id: int):
        pass
