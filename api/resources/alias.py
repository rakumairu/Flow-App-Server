from flask_restful import Resource, request
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class Alias(Resource):
    def get(self):
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)

        # Data unik dari setiap atribut
        unique_data = get_unique_column(data)

        return json.dumps(
            {
                'data': {
                    'column': list(data.columns),
                    'data': unique_data
                },
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
            map_alias(data, args['data']['alias'], args['data']['col'])
            data.to_csv(final_file, index=False)

            unique_data = get_unique_column(data)

            return json.dumps(
                {
                    'data': {
                        'column': list(data.columns),
                        'data': unique_data
                    },
                    'message': 'Succesfully map the data',
                    'status': 'success'
                }
            )
        else:
            return json.dumps(
                {
                    'data': '',
                    'message': 'No data received',
                    'status': 'error'
                }
            )

# Fungsi untuk mengubah alias
def map_alias(data, alias, col):
    data[col] = data[col].map(alias)
    data.dropna(subset=[col], inplace=True)

# Mendapatkan kolom yang unik
def get_unique_column(data):
    unique_data = {}
    for col in data.columns:
        unique_data[col] = list(set(data[col]))

    return unique_data
