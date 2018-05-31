from flask_login import LoginManager
from flask_restplus import Resource
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.models.user_model import users_list

auth_ns = Namespace('auth')

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    for a_user in users_list:
        # In the session, user_id is stored as a unicode character
        # The chr() converts the int id of the user found to unicode for comparing equality
        if chr(a_user.id) == user_id:
            return a_user


class Login(Resource):
    def post(self):
        """
        User Login

        Makes use of Flask-Login

        Use the correct user information to login. Guidelines as stipulated in the register route should be followed

        Note: Only one user can be logged in per client

        """
        pass
