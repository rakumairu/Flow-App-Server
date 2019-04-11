from flask_restful import Resource,reqparse
import werkzeug, os, json

parser = reqparse.RequestParser()
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
_folderPath = './api/static/data/'

class Files(Resource):
    def post(self):
        # TODO: handle return error kalau udah ada filenya
        data = parser.parse_args()
        if data['file'] == None:
            return json.dumps({
                'data': '',
                'message': 'No File Found',
                'status': 'error'
            })
        
        raw_file = data['file']
        if raw_file:
            extension = raw_file.filename.split('.')[-1]
            raw_file.save(os.path.join(_folderPath, 'raw' + '.' + extension))
            return json.dumps({
                'data': '',
                'message': 'File succesfully uploaded',
                'status': 'success'
            })

        return json.dumps({
            'data': '',
            'message': 'Something went wrong',
            'status': 'error'
        })

    def delete(self):
        # TODO: lengkapin deletenya
        raw_csv = os.path.join(_folderPath, 'raw.csv')
        final_csv = os.path.join(_folderPath, 'final.csv')
        if os.path.isfile(raw_csv):
            os.remove(raw_csv)
            if os.path.isfile(final_csv):
                os.remove(final_csv)
            return json.dumps(
                {
                    'data': '',
                    'message': 'File succesfully deleted',
                    'status':  'success'
                }
            )
        else:
            return json.dumps(
                {
                    'data': '',
                    'message': 'File does not exist',
                    'status':  'error'
                }
            )