from flask_restful import Resource, reqparse, request
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class Join(Resource):
    """"Join two columns together"""
    
    def get(self):
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)

        return json.dumps(
            {
                'data': list(data.columns),
                'message': 'Succesfully fetch the data',
                'status': 'success'
            }
        )

    def post(self):
        args = request.get_json(force=True)
        if args != None:
            if os.path.isfile(final_file):
                data = pd.read_csv(final_file)
            else:
                data = pd.read_csv(raw_file)

            join(data, args['data']['col1'], args['data']['col2'], args['data']['name'], args['data']['delimiter'])

            data.to_csv(final_file, index=False)
            return json.dumps(
                {
                    'data': list(data.columns),
                    'message': 'Succesfully join the column',
                    'status': 'success'
                }
            )
        else:
            return json.dumps(
                {
                    'data': '',
                    'message': 'No data received',
                    'status': 'success'
                }
            )

# Fungsi untuk menggabungkan 2 kolom menjadi kolom baru
def join(data, col1, col2, name, delimiter):
    if delimiter != None:
        data[name] = data[col1].map(str) + str(delimiter) + data[col2].map(str)
    else:
        data[name] = data[col1].map(str) + data[col2].map(str)