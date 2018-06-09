from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.database import Database

users_ns = Namespace('users')

db = Database()


class AllUsers(Resource):
    @jwt_required
    @users_ns.doc(security='access_token')
    @users_ns.response(200, "Success")
    @users_ns.response(401, "You are not logged in hence unauthorized")
    @users_ns.response(403, "You are logged in but you are not allowed"
                            " to access this endpoint")
    def get(self):
        """
        Admin View All Users

        ## This route is restricted for administrators' user only
        Admin can view all users
        """
        # the docstring above is for SwaggerUI documentation purposes only

        # return 403 if the user accessing this route is not an administrator
        if current_user['role'] != 'Administrator':
            users_ns.abort(403)

        users_list = []
        try:
            users_list = db.get_all_users()
        except Exception as e:
            users_ns.abort(500, e.args[0])
        output = dict(users=users_list)
        response = self.api.make_response(output, 200)
        return response
