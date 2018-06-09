from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.requests.all_requests import AllRequests
from MaintenanceTrackerAPI.api.v1.requests.single_request import SingleRequest
from MaintenanceTrackerAPI.api.v1.requests.single_request_action import \
    SingleRequestAction

# this is where the namespace, which holds related resources, is instantiated
requests_ns = Namespace('requests', description='Admin routes to view and '
                                                'respond to requests')

requests_ns.add_resource(AllRequests, '/', endpoint='requests')
requests_ns.add_resource(SingleRequest, '/<int:request_id>',
                         endpoint='requests_single_request')
requests_ns.add_resource(SingleRequestAction, '/<int:request_id>'
                                              '/<string:action>',
                         endpoint='requests_single_request_action')
