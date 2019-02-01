from flask_restplus.namespace import Namespace
from MaintenanceTrackerAPI.api.v1.export_swagger\
    .swagger_schema import SwaggerSchema

export_swagger = Namespace('export', description='Exports swagger as a'
                                                 ' json file')

export_swagger.add_resource(SwaggerSchema, '/schema', endpoint='export_schema')
