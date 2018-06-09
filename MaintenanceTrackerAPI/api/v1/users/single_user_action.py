from flask_jwt_extended import jwt_required, current_user
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.database import Database

users_ns = Namespace('users')

db = Database()


class SingleUserAction(Resource):
    @jwt_required
    @users_ns.doc(security='access_token')
    @users_ns.response(200, "Success")
    @users_ns.response(401, "You are not logged in hence unauthorized")
    @users_ns.response(403, "You are logged in but you are not allowed"
                            " to access this endpoint")
    def put(self, user_id: int, action: str):
        """
        Administrator Promote/Demote User

        ## This route is restricted for administrators' user only
        Admin can promote or demote another user
        """
        # the docstring above is for SwaggerUI documentation purposes only

        # return 403 if the user accessing this route is not an administrator
        if current_user['role'] != 'Administrator':
            users_ns.abort(403)

        # check if the action given in URL is recognized by the server
        if action != 'promote' and action != 'demote':
            users_ns.abort(400, 'Action given is not recognized')
        if current_user['user_id'] == user_id:
            users_ns.abort(400, 'You cannot {} yourself'.format(action))

        # retrieve the user of the given id from the database
        this_user = db.get_user_by_id(user_id)
        if not this_user:
            users_ns.abort(400, 'User not found')

        # check whether the user can be promoted/demoted
        if this_user['role'] == 'Administrator' and action == 'promote' \
                or this_user['role'] == 'Consumer' and action == 'demote':
            message = ' is already {}'.format(this_user['role'])
            response = self.api.make_response(dict(
                msg=this_user['email'] + message), 200)
            return response

        # change the role of the user and save it in the database
        new_role_user = db.change_role(action, user_id)

        # return the user and a success message
        message = new_role_user['email'] + ' sucessfully {0}d to {1}'.format(
            action, new_role_user['role']
        )
        response = self.api.make_response(dict(msg=message), 200)
        return response
