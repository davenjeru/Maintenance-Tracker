import datetime

from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.database import db

requests_ns = Namespace('requests')


class SingleRequestAction(Resource):

    @jwt_required
    @requests_ns.doc(security='access_token')
    @requests_ns.response(200, 'Request retrieved successfully')
    @requests_ns.response(400, 'Bad request')
    @requests_ns.response(401, 'Not logged in hence unauthorized')
    @requests_ns.response(403, 'Logged in but forbidden from viewing '
                               'these requests')
    def put(self, request_id: int, action: str):
        """
        Administrator Responds To Request

        ## This route is restricted for administrators' user only
        Allows administrators to respond to a request that has the id given in
        the URL and the action as stated in the URL
        """
        # the docstring above is for SwaggerUI documentation purposes only

        # return 403 if the user accessing this route is not an administrator
        if current_user['role'] != 'Administrator':
            requests_ns.abort(403)

        # the that should be accepted in the URL
        actions = ['approve', 'disapprove', 'reject', 'resolve']
        if action not in actions:
            requests_ns.abort(400, 'action given is not recognized')

        # retrieve the request from the database
        this_request = db.get_request_by_id(request_id)
        if this_request is None:
            requests_ns.abort(404, 'Request not found')

        # create a new request and old request variable which will be
        # dictionaries used in the db.update_request method.
        new_request = dict(request_id=this_request['request_id'],
                           status=None)
        old_request = dict(request_id=this_request['request_id'],
                           status=this_request['status'],
                           last_modified=None)

        if action == 'approve':
            if this_request['status'] != 'Pending Approval':
                requests_ns.abort(409, 'Cannot approve a request that '
                                       'is {}'.format(this_request['status']
                                                      ))
            else:
                new_request['status'] = 'Approved'

        if action == 'disapprove':
            if this_request['status'] != 'Pending Approval':
                requests_ns.abort(409, 'Cannot approve a request that '
                                       'is {}'.format(
                    this_request['status']
                ))
            else:
                new_request['status'] = 'Disapproved'

        if action == 'resolve':
            if this_request['status'] != 'Approved':
                requests_ns.abort(409, 'Cannot approve a request that '
                                       'is {}'.format(this_request['status']
                                                      ))
            else:
                new_request['status'] = 'Resolved'

        # change the 'last_modified' value of this request
        new_request['last_modified'] = datetime.datetime.now()

        # update the changed variables
        db.update_request(new_request, old_request)

        # retrieve the new request from the database and return in response
        # with a message
        new_request = db.get_request_by_id(request_id)
        output = dict(request=new_request)
        output['message'] = 'Request updated successfully'
        response = self.api.make_response(output, 200)
        return response
