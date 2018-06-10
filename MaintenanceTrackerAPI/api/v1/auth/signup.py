from flask_restplus import Resource, fields
from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.boilerplate import get_validated_payload, \
    extract_from_payload, generate_auth_output
from MaintenanceTrackerAPI.api.v1.exceptions import PayloadExtractionError, \
    UserTransactionError
from MaintenanceTrackerAPI.api.v1.models.user_model import User

auth_ns = Namespace('auth')

# Model definition of what to expect from the request data
definition = dict(email=fields.String(title='Your email address',
                                      required=True,
                                      example='myemail@company.com'),
                  password=fields.String(title='Your password',
                                         required=True,
                                         example='password.Pa55word'),
                  confirm_password=fields.String(title='Confirm your password',
                                                 required=True,
                                                 example='password.Pa55word'),
                  security_question=fields.String(title='Your security question'
                                                  , required=True,
                                                  example='What is your'
                                                          ' favourite company?')
                  , security_answer=fields.String(title='Your security answer',
                                                  required=True,
                                                  example='company'))

user_registration_model = auth_ns.model('user_registration_model', definition)


class Register(Resource):
    @auth_ns.expect(user_registration_model)
    @auth_ns.response(201, 'user created successfully')
    @auth_ns.response(415, 'request data not in json format')
    @auth_ns.response(400, 'bad request')
    def post(self):
        """
        User registration

        **Email**
        - email address should be syntactically valid.

        **Password**
        - should have a minimum of **12** characters and a maximum of **80**
        characters
        - should have **no spaces**
        - should have at least **one number**
        - should at least **one uppercase and lowercase letter**.
        - should have at least *one* of these special characters
              !@#$%^;*()_+}{:'?/.,

        **Security Question**
        - will be used if and when a user wants to reset their password
        - should start with a 'Wh' or an 'Are' clause
        - should not contain any punctuations (apart from a compulsory question
         mark '?' at the end)
        - should be between 10 and 50 characters long.

        **Security Answer**
        - should be between 5 and 20 characters long.
        - should not contain any punctuations
        """
        # the docstring above is used by SwaggerUI for documentation

        # This is a short cut for setting all these values to None
        #  with minimal code
        email, password, confirm_password, security_question, \
        security_answer = tuple('    '.split(' '))

        try:
            payload = get_validated_payload(self)
            list_of_names = ['email', 'password', 'confirm_password',
                             'security_question', 'security_answer']
            email, password, confirm_password, security_question, \
            security_answer = extract_from_payload(payload, list_of_names)
        except PayloadExtractionError as e:
            auth_ns.abort(e.abort_code, e.msg)

        # check if password is equal to confirm password
        if password != confirm_password:
            auth_ns.abort(400, 'passwords do not match')

        # try and create the user.
        created_user = None
        try:
            created_user = User(email, password, security_question,
                                security_answer)
        except UserTransactionError as e:
            auth_ns.abort(e.abort_code, e.msg)

        # change the created user object to a dictionary for returning in the
        # response
        user = dict(
            email=created_user.email,
            password_hash=created_user.password_hash,
            security_question=created_user.security_question,
            security_answer_hash=created_user.security_answer_hash,
            role=created_user.role
        )
        output = generate_auth_output(self, user)
        response = self.api.make_response(output, 201)

        return response
