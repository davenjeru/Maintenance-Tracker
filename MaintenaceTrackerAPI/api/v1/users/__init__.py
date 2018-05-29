from flask_restplus.namespace import Namespace

# initiate the namespace
users_ns = Namespace('users', description='Operations related to users')

# add resources related to this namespace and the models in those resource
