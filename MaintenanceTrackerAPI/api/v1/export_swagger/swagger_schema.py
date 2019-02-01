from flask_restplus import Resource
from flask_restplus.namespace import Namespace
from flask import json, send_file
from os import path

export_swagger = Namespace('export')


class SwaggerSchema(Resource):
    @export_swagger.response(200, 'File download started')
    @export_swagger.produces('application/octet-stream')
    def get(self):
        """
        Exports the swagger schema used for this documentation in JSON
        Admin can view all users
        """
        try:
            dirname = path.dirname(path.realpath(__file__))
            file_path = dirname + '/swagger_schema.json'
            file = open(file_path, 'w+')
            json.dump(self.api.__schema__, file, indent=2)
            file.close()
            return send_file(file_path, mimetype='application/octet-stream',
                             as_attachment=True)
        except Exception as e:
            export_swagger.abort(500, e.args[0])
        pass
