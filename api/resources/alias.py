from flask_restful import Resource, request
import pandas as pd, json, os, numpy as np

# Path to raw and final csv
raw_file = 'api/static/data/raw.csv'
final_file = 'api/static/data/final.csv'

class Alias(Resource):
    """"Map alias in a column"""
    
    def get(self):
        """"Handle GET request and return unique data in each columns"""
        
        # Read file to dataframe
        if os.path.isfile(final_file):
            data = pd.read_csv(final_file)
        else:
            data = pd.read_csv(raw_file)

        # Get all unique data in a column
        unique_data = get_unique_column(data)

        # Return data to frontend
        return json.dumps(
            {
                'data': {
                    'column': list(data.columns),
                    'data': unique_data
                },
                'message': 'Succesfully fetch the data',
                'status': 'success'
            }
        )

    def post(self):
        """"Handle POST request"""
        
        # Get arguments from HTTP request
        args = request.get_json(force=True)

        # Check if arguments is null
        if args != None:
            # Read file to dataframe
            if os.path.isfile(final_file):
                data = pd.read_csv(final_file)
            else:
                data = pd.read_csv(raw_file)

            # Check if 'newcolumnname' argument is exist
            if 'newColumnName' in args['data']['alias']:
                # Map data with new column name
                map_alias_new(data, args['data']['alias'], args['data']['col'])
            else:
                # Map data without new column name
                map_alias(data, args['data']['alias'], args['data']['col'])

            # Save data to csv file
            data.to_csv(final_file, index=False)
            # Get unique data again
            unique_data = get_unique_column(data)

            # Return new data if mapping is successful
            return json.dumps(
                {
                    'data': {
                        'column': list(data.columns),
                        'data': unique_data
                    },
                    'message': 'Succesfully map the data',
                    'status': 'success'
                }
            )
        else:
            # Return error
            return json.dumps(
                {
                    'data': '',
                    'message': 'No data received',
                    'status': 'error'
                }
            )

def map_alias(data, alias, col):
    """"Map alias data to certain column without new column name"""
    
    # Map data
    data[col] = data[col].map(alias)
    # Remove any missing value
    data[col].replace('', np.nan, inplace=True)
    data.dropna(subset=[col], inplace=True)

def map_alias_new(data, alias, col):
    """"Map alias data to certain column with new column name"""
    
    # Get new column name
    new_column_name = alias.pop('newColumnName')
    # Copy old data to new column
    data[new_column_name] = data[col]
    # Map data in new column
    data[new_column_name] = data[new_column_name].map(alias)
    # Remove any missing value
    data[col].replace('', np.nan, inplace=True)
    data.dropna(subset=[new_column_name], inplace=True)

def get_unique_column(data):
    """"Return unique column that exist in all columns"""
    
    # New dictionary to store unique data in each columns
    unique_data = {}
    for col in data.columns:
        unique_data[col] = list(set(data[col]))
    return unique_data
