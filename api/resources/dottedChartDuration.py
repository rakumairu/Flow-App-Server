from flask_restful import Resource
import pandas as pd, numpy
import csv, json, os
from datetime import datetime

final_csv = 'api/static/data/final.csv'

class DottedChartDuration(Resource):
    def get(self):
        if os.path.isfile(final_csv):
            df2 = pd.read_csv(final_csv)

            list_case_id = df2['case_id'].unique()
            each_case_list = []
            for x in list_case_id:
                each_case_list.append(df2[df2['case_id'] == x])

            for val in each_case_list:
                duration = []
                temp = None
                xx = None
                for ev in val['timestamp']:
                    if temp != None:
                        if xx == None:
                            xx = date(ev) - date(temp)
                        else:
                            xx += date(ev) - date(temp)
                        dd = datetime.strptime(days_hours_minutes(xx), '%H:%M')
                        duration.append(datetime.strftime(dd, format='%H:%M'))
                    else:
                        dd = datetime.strptime('00:00', '%H:%M')
                        duration.append(datetime.strftime(dd, format='%H:%M'))
                    temp = ev
                val['duration'] = duration

            df2 = pd.concat(each_case_list)

            data2 = {}
            for row in df2.index:
                case_id = df2['case_id'].loc[row]
                task = df2['task'].loc[row]
                timestamp = df2['duration'].loc[row]
                if task not in data2:
                    data2[task] = dict(case_id = [], timestamp = [], size=[])
                if type(case_id) is numpy.int64:
                    data2[task]['case_id'].append(case_id.item())
                else:
                    data2[task]['case_id'].append(case_id)
                data2[task]['timestamp'].append(timestamp)

            sorted_id = []
            for id in list_case_id:
                sorted_id.append(df2[df2['case_id'] == id].tail(1))
            sorted_id = pd.concat(sorted_id)
            sorted_id.sort_values(by=['duration'], inplace=True, ascending=False)
            sorted_id_with_number = {}
            for idx, x in enumerate(sorted_id['case_id'].values.tolist()):
                sorted_id_with_number[x] = idx+1

            return json.dumps(
                {
                    'data': {
                        'data': data2,
                        'sort': sorted_id_with_number
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

def date(datestr):
    temp = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
    return temp

def days_hours_minutes(td):
    return str(td.seconds//3600) + ':' + str((td.seconds//60)%60)