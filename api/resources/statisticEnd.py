from flask_restful import Resource
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class StatisticEnd(Resource):
    """"Return summary statistic for end event"""
    
    def get(self):
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)
        
        if 'case_id' in data.columns and 'task' in data.columns and 'timestamp' in data.columns:
            # List of all the case id
            id_list = list(set(data['case_id']))
            # Get data per id
            data_per_id = {}
            for id in id_list:
                if id not in data_per_id:
                    data_per_id[id] = data[data['case_id'] == id]
            # List start event and end event
            ends = []
            for key, dt in data_per_id.items():
                for x in range(len(dt.index)):
                    if x == len(dt.index)-1:
                        ends.append(dt['task'].iloc[x])
                    elif dt['case_id'].iloc[x+1] != dt['case_id'].iloc[x]:
                        ends.append(dt['task'].iloc[x])
            end_list = list(set(ends))

            # Initialize dictionary to store end event
            end_dict = {}
            # Initialize sum of end event
            total_in_end = 0

            for event in ends:
                if event not in end_dict:
                    end_dict[event] = 1
                    total_in_end+=1
                else:
                    end_dict[event]+=1
                    total_in_end+=1

            # Dictionary occurance start and end event
            end_occurance = []

            for key, item in end_dict.items():
                end = {}
                occurance = item
                percentage = occurance/total_in_end
                end['event'] = key
                end['absolute'] = occurance
                end['relative'] = percentage * 100
                end_occurance.append(end)

            # Sort all value
            end_occurance.sort(key=absoluteColumn, reverse=True)

            return json.dumps(
                {
                    'data': {
                        'end_event': end_list,
                        'end_occurance': end_occurance
                    },
                    'message': 'Succesfully load end event data',
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