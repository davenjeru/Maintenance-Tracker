from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.boilerplate \
    import generate_request_output, extract_from_payload, get_validated_payload, \
    edit_request
from MaintenanceTrackerAPI.api.v1.database import Database
from MaintenanceTrackerAPI.api.v1.exceptions import RequestTransactionError, \
    PayloadExtractionError
from MaintenanceTrackerAPI.api.v1.users.single_user_all_requests \
    import request_model

users_ns = Namespace('users')
db = Database()


class SingleUserSingleRequest(Resource):

    @jwt_required
    @users_ns.doc(security='access_token')
    @users_ns.response(200, 'Request retrieved successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from viewing this request')
    def get(self, request_id: int):
        """
        View One Of Your Requests
        """
        if current_user['role'] == 'Administrator':
            users_ns.abort(403, 'Administrators do not have requests')

        request = db.get_request_by_id(request_id)
        if not request:
            users_ns.abort(404, 'Request not found')
        output = dict(request=request)
        response = self.api.make_response(output, 200)
        return response

    @jwt_required
    @users_ns.doc(security='access_token')
    @users_ns.expect(request_model)
    @users_ns.response(200, 'Request modified successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden'
                            ' from performing this action')
    def patch(self, request_id: int):
        """
        Edit A Request

        - User should be logged in.
        - Your title should have between 10 and 70 characters
        - Your description should have between 40 and 250 characters
        - The request can be sent with title only, description only, or both.
        - If the request is sent with both, they both have to be different
         from the previous title and description
        """
        if current_user['role'] == 'Administrator':
            users_ns.abort(403, 'Administrators do not have requests')

        title, description, this_request, payload = None, None, None, None

        # extract the payload from the response body
        try:
            payload = get_validated_payload(self)
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)

        # extract title from the payload. If it is not found, it remains None
        try:
            title = extract_from_payload(payload, ['title'])
            title = title[0]
        except PayloadExtractionError:
            pass

        # extract description from the payload. If it is not found,
        #  it remains None
        try:
            description = extract_from_payload(payload, ['description'])
            description = description[0]
        except PayloadExtractionError:
            pass

        # create a dictionary of the details collected from payload
        details_dict = dict(title=title, description=description)

        # retrieve request from database
        this_request = db.get_request_by_id(request_id)

        if not this_request:
            users_ns.abort(404, 'Request not found')

        # create a variable 'new_request' which will be a dictionary to be used
        # in db.update_request
        new_request = None
        try:
            new_request = edit_request(this_request, details_dict)
        except RequestTransactionError as e:
            users_ns.abort(e.abort_code, e.msg)

        # update the request in the database. Pass in the new_request and the
        # old request for comparison
        db.update_request(new_request, this_request)
        response = self.api.make_response(
            generate_request_output(self, new_request,
                                    str(self.patch.__name__)), 200)

        return response
