from flask_restful import Resource
import pandas as pd
import json

class Filter(Resource):
    def get(self):
        data = pd.read_csv('api/static/data/raw.csv')
        head = []
        
        for key in data.keys():
            head.append(key)
        
        return json.dumps(head)
    
    def post(self):
        pass