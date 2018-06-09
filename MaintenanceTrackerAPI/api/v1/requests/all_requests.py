from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.database import Database

requests_ns = Namespace('requests')
db = Database()


class AllRequests(Resource):

    @jwt_required
    @requests_ns.doc(security='access_token')
    @requests_ns.response(200, 'Request retrieved successfully')
    @requests_ns.response(400, 'Bad request')
    @requests_ns.response(401, 'Not logged in hence unauthorized')
    @requests_ns.response(403, 'Logged in but forbidden from viewing '
                               'these requests')
    def get(self):
        """
        Administrators View All Requests

        ## This route is restricted for administrator's use only
        Allows administrators to view all requests made in the app
        """
        # the docstring above is for SwaggerUI documentation purposes only

        # return 403 if the user accessing this route is not an administrator
        if current_user['role'] != 'Administrator':
            requests_ns.abort(403)

        # query requests from database and return them
        requests = db.get_requests()
        output = dict(requests=requests)
        response = self.api.make_response(output, 200)
        return response
