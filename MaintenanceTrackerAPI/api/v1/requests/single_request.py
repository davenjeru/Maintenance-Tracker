from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.database import Database

requests_ns = Namespace('requests')

db = Database()


class SingleRequest(Resource):

    @jwt_required
    @requests_ns.doc(security='access_token')
    @requests_ns.response(200, 'Request retrieved successfully')
    @requests_ns.response(400, 'Bad request')
    @requests_ns.response(401, 'Not logged in hence unauthorized')
    @requests_ns.response(403, 'Logged in but forbidden from viewing '
                               'these requests')
    def get(self, request_id):
        if current_user['role'] != 'Administrator':
            requests_ns.abort(403)

        request = db.get_request_by_id(request_id)
        if not request:
            requests_ns.abort(404, 'Request not found')
        output = dict(request=request)
        response = self.api.make_response(output, 200)
        return response
