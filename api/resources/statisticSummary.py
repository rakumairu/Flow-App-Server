from flask_restful import Resource
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class StatisticSummary(Resource):
    def get(self):
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)
        
        if 'case_id' in data.columns and 'task' in data.columns and 'timestamp' in data.columns:
            # Total number of case
            total_case = len(data['case_id'].unique())
            # Total number of event
            total_event = len(data['task'])
            # Total number of unique event
            jenis_event = len(data['task'].unique())

            # All unique event
            all_event = list(set(data['task']))
            # Calculate the occurance of every event
            all_event_occurance = []
            for event in all_event:
                event_occurance = {}
                occurance = len(data[data['task'] == event])
                percentage = occurance / total_event
                event_occurance['event'] = event
                event_occurance['absolute'] = occurance
                event_occurance['relative'] = percentage * 100
                all_event_occurance.append(event_occurance)

            # Sort all value
            all_event_occurance.sort(key=absoluteColumn, reverse=True)

            return json.dumps(
                {
                    'data': {
                        'total_case': total_case,
                        'total_event': total_event,
                        'jenis_event': jenis_event,
                        'event_occurance': all_event_occurance
                    },
                    'message': 'Succesfully load all event data',
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