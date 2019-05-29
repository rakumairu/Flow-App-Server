from flask_restful import Resource, request
import pandas as pd, json, os, numpy as np

# Path to raw and final csv
raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class AlphaMiner(Resource):
    
    def get(self):
        return 'Ini alpha miner'