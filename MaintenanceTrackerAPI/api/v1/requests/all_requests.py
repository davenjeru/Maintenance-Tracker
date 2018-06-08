from flask_restplus import Resource
from flask_restplus.namespace import Namespace

requests_ns = Namespace('requests')


class AllRequests(Resource):
    def get(self):
        pass
