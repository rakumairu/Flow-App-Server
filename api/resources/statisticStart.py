from flask_restful import Resource
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class StatisticStart(Resource):
    """"Return summary statistic for start event"""
    
    def get(self):
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)
        
        if 'case_id' in data.columns and 'task' in data.columns and 'timestamp' in data.columns:
            id_list = list(set(data['case_id']))
            data_per_id = {}
            for id in id_list:
                if id not in data_per_id:
                    data_per_id[id] = data[data['case_id'] == id]
            starts = []
            for key, dt in data_per_id.items():
                for x in range(len(dt.index)):
                    if x == 0:
                        starts.append(dt['task'].iloc[x])
                    elif dt['case_id'].iloc[x-1] != dt['case_id'].iloc[x]:
                        starts.append(dt['task'].iloc[x])
            start_list = list(set(starts))

            start_dict = {}
            total_in_start = 0

            for event in starts:
                if event not in start_dict:
                    start_dict[event] = 1
                    total_in_start+=1
                else:
                    start_dict[event]+=1
                    total_in_start+=1

            # Dictionary occurance start dan end event
            start_occurance = []

            for key, item in start_dict.items():
                start = {}
                occurance = item
                percentage = occurance/total_in_start
                start['event'] = key
                start['absolute'] = occurance
                start['relative'] = percentage * 100
                start_occurance.append(start)

            # Sort all value
            start_occurance.sort(key=absoluteColumn, reverse=True)

            return json.dumps(
                {
                    'data': {
                        'start_event': start_list,
                        'start_occurance': start_occurance
                    },
                    'message': 'Succesfully load start event data',
                    'status': 'success'
                }
            )
        else:
            return json.dumps(
                {
                    'data': '',
                    'message': 'Data is not finished',
                    'status': 'error'
                }
            )

def absoluteColumn(value):
    return value['absolute']