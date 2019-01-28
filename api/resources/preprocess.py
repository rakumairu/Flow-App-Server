from flask_restful import Resource, reqparse
import pandas as pd
import json

parser = reqparse.RequestParser()
parser.add_argument('case_id', type=int)
parser.add_argument('event', type=int)
parser.add_argument('timestamp', type=int)

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class Preprocess(Resource):
    def get(self):
        data = pd.read_csv('api/static/data/raw.csv')
        head = []
        
        for key in data.keys():
            head.append(key)
        
        return json.dumps(
            {
                'data': head,
                'message': 'Succesfully fetch the data',
                'status': 'success'
            }
        )

    def post(self):
        args = parser.parse_args()
        if preprocesses(args['case_id'], args['event'], args['timestamp'], 0) == True:
            return json.dumps(
                {
                    'data': '',
                    'message': 'Succesfully preprocess the data',
                    'status': 'success'
                }
            )
        return json.dumps(
            {
                'data': '',
                'message': 'Something went wrong',
                'status': 'error'
            }
        )

def preprocesses(col_case_id, col_task, col_timestamp, mis_val):
        """"
        Preprocessing raw data
        """
        try:            
            # Load data
            df = pd.read_csv(raw_file)

            # Select column and rename column
            case_id = df.iloc[:, [col_case_id]]
            task = df.iloc[:, [col_task]]
            timestamp = df.iloc[:, [col_timestamp]]

            # Join the column
            df = pd.concat([case_id, task, timestamp], axis=1, sort=False)

            # Rename the column
            df.columns = ['case_id','task','timestamp']

            # Save file to csv format
            df.to_csv(final_file, index=False)

            return True
        except:
            return False