from flask_login import login_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.boilerplate import check_id_availability, \
    PayloadExtractionError, safe_request_output, generate_request_output, extract_from_payload, get_validated_payload
from MaintenanceTrackerAPI.api.v1.models.request_model import requests_list, Request, RequestTransactionError
from MaintenanceTrackerAPI.api.v1.models.user_model import users_list, User
from MaintenanceTrackerAPI.api.v1.users.single_user_all_requests import request_model

users_ns = Namespace('users')


class SingleUserSingleRequest(Resource):

    @login_required
    @users_ns.response(200, 'Request retrieved successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from viewing this request')
    def get(self, user_id: int, request_id: int):
        """
        View a single request from a specific user
        """

        if current_user.role != 'Administrator' and current_user.id != user_id:
            users_ns.abort(403)

        try:
            check_id_availability(user_id, users_list, str(User.__name__))
            check_id_availability(request_id, requests_list, str(Request.__name__))
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)

        for request in requests_list:
            if request.user_id == user_id and request.id == request_id:
                output = dict(request=safe_request_output(self,
                                                          check_id_availability(request_id, requests_list,
                                                                                str(Request.__name__))))
                return output
        else:
            users_ns.abort(400, 'the requested user does not own this request')

    @login_required
    @users_ns.expect(request_model)
    @users_ns.response(200, 'Request modified successfully')
    @users_ns.response(400, 'Bad request')
    @users_ns.response(401, 'Not logged in hence unauthorized')
    @users_ns.response(403, 'Logged in but forbidden from performing this action')
    def patch(self, user_id: int, request_id: int):
        """
        Modify a request

        1. User should be logged in.
        2. Your title should have between 10 and 70 characters
        3. Your description should have between 40 and 500 characters
        4. The request can be sent with title only, description only, or both.
        5. If the request is sent with both, they both have to be different from the previous title and description
        """

        if current_user.id != user_id:
            users_ns.abort(403)

        title, description, this_request, payload = None, None, None, None
        try:
            check_id_availability(user_id, users_list, str(User.__name__))
            this_request = check_id_availability(request_id, requests_list, str(Request.__name__))
            payload = get_validated_payload(self)
        except PayloadExtractionError as e:
            users_ns.abort(e.abort_code, e.msg)

        try:
            title = extract_from_payload(payload, ['title'])
            title = title[0]
        except PayloadExtractionError:
            pass

        try:
            description = extract_from_payload(payload, ['description'])
            description = description[0]
        except PayloadExtractionError:
            pass

        details_dict = dict(title=title, description=description)

        try:
            this_request = this_request.edit(current_user, details_dict)
        except RequestTransactionError as e:
            users_ns.abort(e.abort_code, e.msg)

        response = self.api.make_response(generate_request_output(self, this_request, str(self.patch.__name__)), 200)
        response.headers['location'] = self.api.url_for(SingleUserSingleRequest, user_id=user_id, request_id=request_id)

        return response
