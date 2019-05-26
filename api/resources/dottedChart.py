from flask_restful import Resource
import pandas as pd, numpy
import csv, json, os

final_csv = 'api/static/data/final.csv'

class DottedChart(Resource):
    """"Process the data to display dotted chart with absolute time"""
    
    def get(self):
        if os.path.isfile(final_csv):
            df = pd.read_csv(final_csv)
            # Used to store the data
            data = dict()
            for row in df.index:
                # Get case id, task and timestamp
                case_id = df['case_id'].loc[row]
                task = df['task'].loc[row]
                timestamp = df['timestamp'].loc[row]
                if task not in data:
                    # Initialize data
                    data[task] = dict(case_id = [], timestamp = [])
                # Insert case id to data
                if type(case_id) is numpy.int64:
                    data[task]['case_id'].append(case_id.item())
                else:
                    data[task]['case_id'].append(case_id)
                # Insert timestamp to data
                data[task]['timestamp'].append(timestamp)

            # Used to sort the case id
            sort_cid = {}
            for idx, x in enumerate(list(reversed(df['case_id'].unique().tolist()))):
                sort_cid[x] = idx+1
            return json.dumps(
                {
                    'data': {
                        'data': data,
                        'sort': sort_cid
                    },
                    'message': 'Succesfully load dotted chart with absolute time',
                    'status': 'success'
                }
            )
        else:
            return json.dumps(
                {
                    'data': '',
                    'message': 'File not found',
                    'status': 'error'
                }
            )
