from flask_restful import Resource
import os, json


class FileExist(Resource):
    """"Check if file is exist in server or not"""
    
    def get(self):
        if os.path.isfile('api/static/data/raw.csv'):
            return json.dumps(
                {
                    'data': '',
                    'message': 'File exist',
                    'status': 'success'
                }
            )
        return json.dumps(
            {
                'data': '',
                'message': 'File does not exist',
                'status': 'error'
            }
        )