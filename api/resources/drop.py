from flask_restful import Resource, reqparse, request
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class Drop(Resource):
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

            drop(data, args['data']['col'])

            data.to_csv(final_file, index=False)
            return json.dumps(
                {
                    'data': list(data.columns),
                    'message': 'Succesfully drop the column',
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

def drop(data, col):
    data.drop(col, axis=1, inplace=True)