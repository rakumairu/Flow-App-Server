from flask_restful import Resource, reqparse, request
from datetime import datetime
import pandas as pd, json, os, numpy as np

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class CountAttempt(Resource):
    """"Count quiz attempt by student"""

    def get(self):
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)

        # Get unique data
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

            # Do the process to count the quiz attempt
            do(data, args['data']['col'], args['data']['start'], args['data']['end'], args['data']['base'])

            # Get unique data
            unique_data = get_unique_column(data)

            return json.dumps(
            {
                'data': {
                    'column': list(data.columns),
                    'data': unique_data
                },
                'message': 'Succesfully count the attempt',
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

def do(df, col, start, end, base):
    """"Count quiz attempt"""

    # Get unique id
    id_list = df[base].unique()

    # Store data per id
    data_per_id = dict()
    for id in id_list:
        if id not in data_per_id:
            data_per_id[id] = df[df[base] == id]

    # Count the attempt
    list_of_data = []
    for key, data in data_per_id.items():
        dt = data
        time_id_list = []
        id = np.nan
        iter = 0
        for x in range(len(dt.index)):
            if dt[col].iloc[x] == start:
                iter+=1
                # id = str(dt[base].iloc[x]) + '_' + str(iter)
                id = str(iter)
            elif x != 0:
                if dt[col].iloc[x-1] == end:
                    id = np.nan
            time_id_list.append(id)
        dt['n_attempt'] = time_id_list
        dt.dropna(subset=['n_attempt'], inplace=True)
        list_of_data.append(dt)

    # Concatenate all the data
    df = pd.concat(list_of_data)
    # Sort the index
    df.sort_index(inplace=True)
    df.to_csv(final_file, index=False)

def get_unique_column(data):
    """"Get unique column"""
    
    unique_data = {}
    for col in data.columns:
        unique_data[col] = list(set(data[col]))
    return unique_data