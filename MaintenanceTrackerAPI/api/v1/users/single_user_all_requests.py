from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.boilerplate import generate_request_output, \
    get_validated_payload, extract_from_payload
from MaintenanceTrackerAPI.api.v1.exceptions import PayloadExtractionError, \
    RequestTransactionError
from MaintenanceTrackerAPI.api.v1.models.request_model import Request

users_ns = Namespace('users')
request_model = users_ns.model('request_model', {
    'request_type': fields.String(
        title='The request type. Can be \'Maintenance\''
              ' or \'Repair\'. Defaults to \'Repair\' if left empty.',
        required=False,
        example='Repair'),
    'title': fields.String(title='The title of your request', required=True,
                           example='My Request Title'),
    'description': fields.String(title='The description of your request',
                                 required=True,
                                 example='An explanation of what happened'
                                         ' to justify this request.')
})


class SingleUserAllRequests(Resource):
    @users_ns.response(200, "Success")
    @users_ns.response(401, "You are not logged in hence unauthorized")
    @users_ns.response(403, "You are logged in but you are not allowed"
                            " to access this endpoint")
    def get(self, user_id: int):
        """
        View all requests from a single user
        """
        # abort with 403 if the user is not an administrator or the id
        # stored in the session is not equal to the id in the route
        current_user = None
        if current_user.id != user_id and current_user.role != 'Administrator':
            users_ns.abort(403)

        if current_user.id == user_id and current_user.role == 'Administrator':
            users_ns.abort(400, 'Administrators do not have requests')
        pass

    @users_ns.expect(request_model)
    @users_ns.response(201, 'Request made successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403,
                       'Logged in but forbidden from performing this action')
    def post(self, user_id: int):
        """
        Make a request

        1. User must be logged in to make a request
        2. Your title should have between 10 and 70 characters
        3. Your description should have between 40 and 250 characters
        4. Duplicate requests will not be created

        """
        current_user = None

        if current_user.id != user_id:
            users_ns.abort(403)

        title, description, request_type = None, None, None

        try:
            payload = get_validated_payload(self)
            list_of_names = ['request_type', 'title', 'description']
            request_type, title, description = extract_from_payload(
                payload, list_of_names)
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)

        request = None
        try:
            request = Request(current_user, request_type, title, description)
        except RequestTransactionError as e:
            users_ns.abort(e.abort_code, e.msg)
        output = generate_request_output(self, request, 'post')
        response = self.api.make_response(output, 201)
        return response
