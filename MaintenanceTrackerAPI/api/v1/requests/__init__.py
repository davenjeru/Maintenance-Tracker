from flask_restplus.namespace import Namespace

from MaintenanceTrackerAPI.api.v1.requests.all_requests import AllRequests
from MaintenanceTrackerAPI.api.v1.requests.single_request import SingleRequest

requests_ns = Namespace('requests', description='Admin routes to view and '
                                                'respond to requests')

requests_ns.add_resource(AllRequests, '/')
requests_ns.add_resource(SingleRequest, '/<int:request_id>')
