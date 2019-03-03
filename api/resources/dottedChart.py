from flask_restful import Resource
import pandas as pd, numpy
import csv, json, os

final_csv = 'api/static/data/final.csv'

class DottedChart(Resource):
    def get(self):
        if os.path.isfile(final_csv):
            df = pd.read_csv(final_csv)
            data = dict()
            for row in df.index:
                case_id = df['case_id'].loc[row]
                task = df['task'].loc[row]
                timestamp = df['timestamp'].loc[row]
                if task not in data:
                    data[task] = dict(case_id = [], timestamp = [])
                if type(case_id) is numpy.int64:
                    data[task]['case_id'].append(case_id.item())
                else:
                    data[task]['case_id'].append(case_id)
                data[task]['timestamp'].append(timestamp)

            sort_cid = {}
            for idx, x in enumerate(list(reversed(df['case_id'].unique().tolist()))):
                sort_cid[x] = idx+1
            return json.dumps(
                {
                    'data': {
                        'data': data,
                        'sort': sort_cid
                    },
                    'message': 'Succesfully fetch the data',
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
