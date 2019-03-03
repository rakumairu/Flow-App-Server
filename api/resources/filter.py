from flask_restful import Resource, request
import pandas as pd, json, os

raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class Filter(Resource):
    def get(self):
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)

        if 'case_id' in data.columns and 'task' in data.columns and 'timestamp' in data.columns:
            # Semua event yang unik
            all_event = list(set(data['task']))

            # List dari semua id
            id_list = list(set(data['case_id']))
            # Mengambil data per id
            data_per_id = {}
            for id in id_list:
                if id not in data_per_id:
                    data_per_id[id] = data[data['case_id'] == id]
            # List start event dan end event
            start_list = []
            end_list = []
            for key, dt in data_per_id.items():
                for x in range(len(dt.index)):
                    if x == 0:
                        start_list.append(dt['task'].iloc[x])
                    elif dt['case_id'].iloc[x-1] != dt['case_id'].iloc[x]:
                        start_list.append(dt['task'].iloc[x])
                    elif x == len(dt.index)-1:
                        end_list.append(dt['task'].iloc[x])
                    elif dt['case_id'].iloc[x+1] != dt['case_id'].iloc[x]:
                        end_list.append(dt['task'].iloc[x])
            start_list = list(set(start_list))
            end_list = list(set(end_list))

            return json.dumps(
                {
                    'data': {
                        'start': start_list,
                        'end': end_list,
                        'all': all_event
                    },
                    'message': 'Succesfully fetch the data',
                    'status': 'success'
                }
            )

        else:
            return json.dumps(
                {
                    'data':'',
                    'message': 'Data is not finished',
                    'status': 'error'
                }
            )
        pass
    
    def post(self):
        args = request.get_json(force=True)
        if args != None:
            if os.path.isfile(final_file):
                data = pd.read_csv(final_file)
            else:
                data = pd.read_csv(raw_file)

            try:
                start = args['data']['start']

                # Kolom untuk sort data ulang
                data['Sort'] = list([x for x in range(0,len(data['case_id']))])

                # List dari semua id
                id_list = data['case_id'].unique()

                # Mengambil data per id
                data_per_id = dict()
                for id in id_list:
                    if id not in data_per_id:
                        data_per_id[id] = data[data['case_id'] == id]

                # List of selected start event
                list_of_data = []
                for key, dt in data_per_id.items():
                    for ev in start:
                        if dt['task'].iloc[0] == ev:
                            list_of_data.append(dt)

                data = pd.concat(list_of_data)
                data.sort_values('Sort', inplace=True)
                data.drop('Sort', axis=1, inplace=True)
                data.to_csv(final_file, index=False)

                return json.dumps(
                    {
                        'data': '',
                        'message': 'Success filtering the data',
                        'status': 'success'
                    }
                )
            except KeyError as ke:
                print(ke)

            try:
                end = args['data']['end']

                # Kolom untuk sort data ulang
                data['Sort'] = list([x for x in range(0,len(data['case_id']))])

                # List dari semua id
                id_list = data['case_id'].unique()

                # Mengambil data per id
                data_per_id = dict()
                for id in id_list:
                    if id not in data_per_id:
                        data_per_id[id] = data[data['case_id'] == id]

                # List selected end event
                list_of_data = []
                for key, dt in data_per_id.items():
                    for ev in end:
                        if dt['task'].iloc[-1] == ev:
                            list_of_data.append(dt)

                data = pd.concat(list_of_data)
                data.sort_values('Sort', inplace=True)
                data.drop('Sort', axis=1, inplace=True)
                data.to_csv(final_file, index=False)

                return json.dumps(
                    {
                        'data': '',
                        'message': 'Success filtering the data',
                        'status': 'success'
                    }
                )
            except KeyError as ke:
                print(ke)

            try:
                all = args['data']['all']

                # Kolom untuk sort data ulang
                data['Sort'] = list([x for x in range(0,len(data['case_id']))])

                list_data = []
                for idx, ev in enumerate(data['task']):
                    for evt in all:
                        if ev == evt:
                            list_data.append(data.iloc[idx])

                data = pd.DataFrame(list_data)
                data.sort_values('Sort', inplace=True)
                data.drop('Sort', axis=1, inplace=True)
                data.to_csv(final_file, index=False)

                return json.dumps(
                    {
                        'data': '',
                        'message': 'Success filtering the data',
                        'status': 'success'
                    }
                )
            except KeyError as ke:
                print(ke)
        else:
            return json.dumps(
                {
                    'data': '',
                    'message': 'Failed filtering the data',
                    'status': 'error'
                }
            )