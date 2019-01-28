from flask_restful import Resource
import json, os
import pandas as pd

class Display(Resource):
    def get(self):
        if os.path.isfile('api/static/data/raw.csv'):
            # RAW FILE
            data = pd.read_csv('api/static/data/raw.csv')

            # Mengambil header dari file
            head = list(data.columns.values)

            # Inisialisasi data untuk json
            raw = []

            # TODO: handle kalo data NaN di ganti jadi none atau sejenisnya

            for el in data.values:
                row = {}
                for e in range(0, len(el)):
                    row[head[e]] = el[e]
                raw.append(row)
            
            # Header data
            raw_head = []
            for k in data.keys():
                raw_head.append(k)

            if os.path.isfile('api/static/data/final.csv'):
                # FINAL FILE
                data = pd.read_csv('api/static/data/final.csv')

                # Mengambil header dari file
                head = list(data.columns.values)

                # Inisialisasi data untuk json
                final = []

                # TODO: handle kalo data NaN di ganti jadi none atau sejenisnya

                for el in data.values:
                    row = {}
                    for e in range(0, len(el)):
                        row[head[e]] = el[e]
                    final.append(row)
                
                # Header data
                final_head = []
                for k in data.keys():
                    final_head.append(k)

                return json.dumps(
                    {
                        'data': {
                            "raw": {"data": raw, "head": raw_head}, 
                            "final": {"data": final, "head": final_head}
                    },
                        'message': 'Succesfully fetch the data',
                        'status': 'success'
                    }
                )

            return json.dumps(
                {
                    'data': {
                        "raw": {"data": raw, "head":raw_head}
                    },
                    'message': 'Succesfully fetch the data',
                    'status': 'success'
                }
            )
        return json.dumps(
            {
                'data': '',
                'message': 'File not found, please upload it first',
                'status': 'error'
            }
        )