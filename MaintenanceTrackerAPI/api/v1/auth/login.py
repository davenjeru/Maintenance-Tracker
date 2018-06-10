from flask_jwt_extended import JWTManager, create_access_token
from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace
from werkzeug.security import check_password_hash

from MaintenanceTrackerAPI.api.v1.boilerplate import extract_from_payload, \
    get_validated_payload, generate_auth_output
from MaintenanceTrackerAPI.api.v1.database import db
from MaintenanceTrackerAPI.api.v1.exceptions import PayloadExtractionError

# this is where I first use jwt, so decided to initiate it here
jwt = JWTManager()

# call the namespace that this resource belongs to
auth_ns = Namespace('auth')

# define the login model. This is solely used by SwaggerUI for documentation
user_login_model = auth_ns.model('user_login_model', {
    'email': fields.String(title='Your email address', required=True,
                           example='myemail@company.com'),
    'password': fields.String(title='Your email address', required=True,
                              example='password.Pa55word')
})


class Login(Resource):
    @auth_ns.expect(user_login_model)
    @auth_ns.response(200, 'user logged in successfully')
    @auth_ns.response(415, 'request data not in json format')
    @auth_ns.response(401, 'invalid password')
    @auth_ns.response(400, 'bad request')
    def post(self):
        """
        User Login

        - Makes use of Flask-JWT-Extended
        - Use the correct user information to login. Guidelines as stipulated
        in the register route should be followed
        - Note: You will receive a token which you will need to put in the header
        as ACCESS_TOKEN so as to reach protected endpoints

        """

        email, password = None, None
        # try and extract email, and password from the request body
        try:
            payload = get_validated_payload(self)
            list_of_names = ['email', 'password']
            email, password = extract_from_payload(payload, list_of_names)
        except PayloadExtractionError as e:
            auth_ns.abort(e.abort_code, e.msg)

        # get user from the database
        this_user = db.get_user_by_email(email)

        # return user not found if None
        if not this_user:
            auth_ns.abort(404, 'User not found')

        # check if the password is okay
        if not check_password_hash(this_user['password_hash'], password):
            auth_ns.abort(401, 'invalid password')

        # password is valid so we give them an access token.
        output = generate_auth_output(self, this_user)
        identity = dict(user_id=this_user['user_id'],
                        email=this_user['email'],
                        role=this_user['role'])
        output['access_token'] = create_access_token(identity)
        response = self.api.make_response(output, 200)
        return response
