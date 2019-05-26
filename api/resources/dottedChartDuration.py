from flask_restful import Resource
import pandas as pd, numpy
import csv, json, os
from datetime import datetime, timedelta

final_csv = 'api/static/data/final.csv'

class DottedChartDuration(Resource):
    """"Process the data ti display dotted chart with relative time"""
    
    def get(self):
        if os.path.isfile(final_csv):
            df2 = pd.read_csv(final_csv)

            # Get unique case id
            list_case_id = df2['case_id'].unique()
            # Get data for every case id
            each_case_list = []
            for x in list_case_id:
                each_case_list.append(df2[df2['case_id'] == x])

            for val in each_case_list:
                # Used to store duration
                duration = []
                # Offset time
                duplicate_offset = 1
                # Flag for duplicate time in 1 case id
                duplicate_flag = False
                # Temporary value to store previous time
                temp = None
                # Value of difference in time
                xx = None
                # Get every timestamp value
                for ev in val['timestamp']:
                    if temp != None:
                        if xx == None:
                            # Store the difference between current and previous time
                            xx = date(ev) - date(temp)
                        else:
                            xx += date(ev) - date(temp)
                        if ev == temp:
                            if duplicate_flag == False:
                                duplicate_offset = 0
                                duplicate_flag = True
                            # Increase the offset
                            duplicate_offset += 1
                            # Add offset to current duration
                            yy = xx + timedelta(seconds = duplicate_offset)
                        else:
                            duplicate_flag = False
                            yy = xx + timedelta(seconds = 0)
                        # Get duration format
                        dd = datetime.strptime(days_hours_minutes(yy), '%H:%M:%S')
                        duration.append(datetime.strftime(dd, format='%H:%M:%S'))
                    else:
                        dd = datetime.strptime('00:00:00', '%H:%M:%S')
                        duration.append(datetime.strftime(dd, format='%H:%M:%S'))
                    temp = ev
                # Create duration column
                val['duration'] = duration

            # Concatenate all the data
            df2 = pd.concat(each_case_list)
            df2.to_csv('api/static/data/coba.csv', index=False)

            data2 = {}
            for row in df2.index:
                case_id = df2['case_id'].loc[row]
                task = df2['task'].loc[row]
                timestamp = df2['duration'].loc[row]
                if task not in data2:
                    data2[task] = dict(case_id = [], timestamp = [])
                if type(case_id) is numpy.int64:
                    data2[task]['case_id'].append(case_id.item())
                else:
                    data2[task]['case_id'].append(case_id)
                data2[task]['timestamp'].append(timestamp)

            # Used to store sorted id
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
                    'message': 'Succesfully load dotted chart with relative time',
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
    """"Change time format"""
    
    temp = datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
    return temp

def days_hours_minutes(td):
    """"Get seconds from days hours and minutes"""
    
    return str(td.seconds//3600) + ':' + str((td.seconds//60)%60) + ':' + str(td.seconds%60)