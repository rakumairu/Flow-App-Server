from flask_restful import Resource, reqparse, request
from datetime import datetime
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class ConvertTime(Resource):
    """"Convert time formatting"""

    def get(self):
        """"Handle GET request"""

        # Read file to dataframe
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)

        # Return data to frontend
        return json.dumps(
            {
                'data': list(data.columns),
                'message': 'Succesfully fetch the data',
                'status': 'success'
            }
        )

    def post(self):
        """"Handle POST request"""

        # Store argument from HTTP request
        args = request.get_json(force=True)

        # Check if arguments is empty
        if args != None:
            # Read file to dataframe
            if os.path.isfile(final_file):
                data = pd.read_csv(final_file)
            else:
                data = pd.read_csv(raw_file)

            try:
                # Convert time format
                convert(data, args['data']['time'])
            except Exception as e:
                print(e)
                return json.dumps(
                    {
                        'data': '',
                        'message': 'Something went wrong',
                        'status': 'error'
                    }
                )

            data.to_csv(final_file, index=False)
            return json.dumps(
                {
                    'data': list(data.columns),
                    'message': 'Succesfully convert the data',
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

def convert(df, col):
    """"Convert formatting time"""

    temp = []
    for i, x in enumerate(df[col]):
        d = datetime.strptime(x, '%d/%m/%y, %H:%M')
        temp.append(d)

    df[col] = temp