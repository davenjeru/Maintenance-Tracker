from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.database import Database

users_ns = Namespace('users')
db = Database()


class SingleUser(Resource):
    @jwt_required
    @users_ns.doc(security='access_token')
    @users_ns.response(200, "Success")
    @users_ns.response(401, "You are not logged in hence unauthorized")
    @users_ns.response(403, "You are logged in but you are not allowed"
                            " to access this endpoint")
    def get(self, user_id: int):
        """
        Admin View One User

        ## This route is restricted for administrators' user only
        Admin can view one user as per the id given in the URL
        """
        # the docstring above is for SwaggerUI documentation purposes only

        # return 403 if the user accessing this route is not an administrator
        if current_user['role'] != 'Administrator':
            users_ns.abort(403)

        user = None
        try:
            user = db.get_user_by_id(user_id)
        except Exception as e:
            users_ns.abort(500, e.args[0])

        if not user:
            users_ns.abort(404, 'User not found')

        output = dict(user=user)
        response = self.api.make_response(output, 200)
        return response
