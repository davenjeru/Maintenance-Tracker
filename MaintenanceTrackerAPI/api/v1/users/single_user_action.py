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
        if current_user['role'] != 'Administrator':
            users_ns.abort(403)

        if action != 'promote' and action != 'demote':
            users_ns.abort(400, 'Action given is not recognized')
        if current_user['user_id'] == user_id:
            users_ns.abort(400, 'You cannot {} yourself'.format(action))

        this_user = db.get_user_by_id(user_id)
        if not this_user:
            users_ns.abort(400, 'User not found')

        if this_user['role'] == 'Administrator' and action == 'promote' \
                or this_user['role'] == 'Consumer' and action == 'demote':
            message = ' is already {}'.format(this_user['role'])
            response = self.api.make_response(dict(
                msg=this_user['email'] + message), 200)
            return response

        new_role_user = db.change_role(action, user_id)
        message = new_role_user['email'] + ' sucessfully {0}d to {1}'.format(
            action, new_role_user['role']
        )
        response = self.api.make_response(dict(msg=message), 200)
        return response
