from flask_restplus import Resource
from flask_restplus.namespace import Namespace

requests_ns = Namespace('requests')


class SingleRequest(Resource):
    def get(self):
        pass
