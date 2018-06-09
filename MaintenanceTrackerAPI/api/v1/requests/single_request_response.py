import datetime

from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.database import Database

requests_ns = Namespace('requests')

db = Database()


class SingleRequestResponse(Resource):

    @jwt_required
    @requests_ns.doc(security='access_token')
    @requests_ns.response(200, 'Request retrieved successfully')
    @requests_ns.response(400, 'Bad request')
    @requests_ns.response(401, 'Not logged in hence unauthorized')
    @requests_ns.response(403, 'Logged in but forbidden from viewing '
                               'these requests')
    def put(self, request_id: int, response: str):
        if current_user['role'] != 'Administrator':
            requests_ns.abort(403)

        responses = ['approve', 'disapprove', 'reject', 'resolve']
        if response not in responses:
            requests_ns.abort(400, 'response given is not recognized')

        this_request = db.get_request_by_id(request_id)
        if this_request is None:
            requests_ns.abort(404, 'Request not found')

        new_request = dict(request_id=this_request['request_id'],
                           status=None)
        old_request = dict(request_id=this_request['request_id'],
                           status=this_request['status'],
                           last_modified=None)

        if response == 'approve':
            if this_request['status'] != 'Pending Approval':
                requests_ns.abort('Cannot approve a request that is {}'.format(
                    this_request['status']
                ))
            else:
                new_request['status'] = 'Approved'

        if response == 'disapprove':
            if this_request['status'] != 'Pending Approval':
                requests_ns.abort('Cannot approve a request that is {}'.format(
                    this_request['status']
                ))
            else:
                new_request['status'] = 'Disapproved'

        if response == 'resolve':
            if this_request['status'] != 'Approved':
                requests_ns.abort('Cannot approve a request that is {}'.format(
                    this_request['status']
                ))
            else:
                new_request['status'] = 'Resolved'
        new_request['last_modified'] = datetime.datetime.now()
        db.update_request(new_request, old_request)
        new_request = db.get_request_by_id(request_id)
        output = dict(request=new_request)
        output['message'] = 'Request updated successfully'
        response = self.api.make_response(output, 200)
        return response
