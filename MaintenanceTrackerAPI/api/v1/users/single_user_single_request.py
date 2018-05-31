from flask_login import login_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.boilerplate import check_id_availability, \
    PayloadExtractionError, safe_request_output
from MaintenanceTrackerAPI.api.v1.models.request_model import requests_list, Request
from MaintenanceTrackerAPI.api.v1.models.user_model import users_list, User

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
                output = None
                try:
                    output = dict(request=safe_request_output(self,
                                                              check_id_availability(request_id,
                                                                                    requests_list,
                                                                                    str(Request.__name__))))
                    return output
                except PayloadExtractionError as e:
                    users_ns.abort(e.abort_code, e.msg)
        else:
            users_ns.abort(400, 'the requested user does not own this request')
