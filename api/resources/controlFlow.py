from flask_restful import Resource
import csv, json

class ControlFlow(Resource):
    def get(self):
        try:
            log = flow(csv_to_dict('api/static/data/final.csv'))
            
            max, min = find_max_min(log)

            return json.dumps(
                {
                    'data': {
                        'log': log,
                        'max': max,
                        'min': min
                    },
                    'message': 'Succesfully fetch the data',
                    'status': 'success'
                }
            )
        except:
            return json.dumps(
                {
                    'data': '',
                    'message': 'Something went wrong',
                    'status': 'error'
                }
            )
    
def csv_to_dict(file_path):
    """"
    Read csv file as Python dictionary
    """
    # Initialize dictionary
    log = dict()

    # Read csv file
    with open(file_path, newline='') as csv_file:
        # Initialize csv reader
        f = csv.reader(csv_file, delimiter=',', quotechar='|')
        # Get next value
        next(f)
        for line in f:
            # Get case id, task and timestamp value
            case_id = line[0]
            task = line[1]
            timestamp = line[2]

            # Initialize log for each case_id
            if case_id not in log:
                log[case_id] = []

            event = (task, timestamp)
            log[case_id].append(event)
    
    # Return dictionary
    return log

def flow(eLog):
    """"
    Flow Algorithm to count transaction that exist in the process
    """
    # Initialize dictionary
    F = dict()

    # For each case_id in event_log
    for case_id in eLog:
        # For each transition in event_log
        for i in range(0, len(eLog[case_id])-1): #-1 so it won't return outofindex error
            # Current case_id
            a1 = eLog[case_id][i][0]
            # Next case_id
            a2 = eLog[case_id][i+1][0]

            # Initialize the second dimension of the dictionary
            if a1 not in F:
                F[a1] = dict()
            if a2 not in F[a1]:
                F[a1][a2] = 0

            F[a1][a2] += 1
    
    # Return the dictionary
    return F

def find_max_min(eLog):
    """"
    Finding maximum and minimum value in the data
    """
    # Initialize max and min value
    max = 0
    min = float('inf')
    for task in eLog:
        for task2 in eLog[task]:
            val = eLog[task][task2]
            if max < val:
                max = val
            if min > val:
                min = val
    return max, min