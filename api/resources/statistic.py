from flask_restful import Resource
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class Statistic(Resource):
    def get(self):
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)
        
        if len(data.columns) == 3:
            # Jumlah case
            total_case = len(data['case_id'].unique())
            # Jumlah event total
            total_event = len(data['task'])
            # Jumlah event unique
            jenis_event = len(data['task'].unique())

            # Semua event yang unik
            all_event = list(set(data['task']))
            # Menghitung occurance dari setiap event
            all_event_occurance = []
            for event in all_event:
                event_occurance = {}
                occurance = len(data[data['task'] == event])
                percentage = occurance / total_event
                event_occurance['event'] = event
                event_occurance['absolute'] = occurance
                event_occurance['relative'] = percentage * 100
                all_event_occurance.append(event_occurance)

            # List dari semua id
            id_list = list(set(data['case_id']))
            # Mengambil data per id
            data_per_id = {}
            for id in id_list:
                if id not in data_per_id:
                    data_per_id[id] = data[data['case_id'] == id]
            # List start event dan end event
            starts = []
            ends = []
            for key, dt in data_per_id.items():
                for x in range(len(dt.index)):
                    if x == 0:
                        starts.append(dt['task'].iloc[x])
                    elif dt['case_id'].iloc[x-1] != dt['case_id'].iloc[x]:
                        starts.append(dt['task'].iloc[x])
                    elif x == len(dt.index)-1:
                        ends.append(dt['task'].iloc[x])
                    elif dt['case_id'].iloc[x+1] != dt['case_id'].iloc[x]:
                        ends.append(dt['task'].iloc[x])
            start_list = list(set(starts))
            end_list = list(set(ends))

            # Dictionary jumlah start dan end event
            start_dict = {}
            end_dict = {}
            total_in_start = 0
            total_in_end = 0

            for event in starts:
                if event not in start_dict:
                    start_dict[event] = 1
                    total_in_start+=1
                else:
                    start_dict[event]+=1
                    total_in_start+=1
                    
            for event in ends:
                if event not in end_dict:
                    end_dict[event] = 1
                    total_in_end+=1
                else:
                    end_dict[event]+=1
                    total_in_end+=1
            # Dictionary occurance start dan end event
            start_occurance = []
            end_occurance = []

            for key, item in start_dict.items():
                start = {}
                occurance = item
                percentage = occurance/total_in_start
                start['event'] = key
                start['absolute'] = occurance
                start['relative'] = percentage * 100
                start_occurance.append(start)
                
            for key, item in end_dict.items():
                end = {}
                occurance = item
                percentage = occurance/total_in_end
                end['event'] = key
                end['absolute'] = occurance
                end['relative'] = percentage * 100
                end_occurance.append(end)

            # Sort all value
            all_event_occurance.sort(key=absoluteColumn, reverse=True)
            start_occurance.sort(key=absoluteColumn, reverse=True)
            end_occurance.sort(key=absoluteColumn, reverse=True)

            return json.dumps(
                {
                    'data': {
                        'total_case': total_case,
                        'total_event': total_event,
                        'jenis_event': jenis_event,
                        'event_occurance': all_event_occurance,
                        'start_event': start_list,
                        'end_event': end_list,
                        'start_occurance': start_occurance,
                        'end_occurance': end_occurance
                    },
                    'message': 'Succesfully fetch the data',
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