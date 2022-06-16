""" 
This snippet is similar to the one in parse_gsheets.py
but assumes that the gsheet creds have been downloaded as a pickle file
"""

import pandas as pd
import pickle
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    
creds = pickle.loads("path/token.pickle")

def lambda_handler(event, context):
    spreadsheet_id = 'spreadsheet_id'
    range_name = 'range_name'
    header_row = 0
    data_row_start = 2
    
    service = build('sheets', 'v4', credentials=creds)
    gsheet = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()

    header = gsheet.get('values', [])[header_row]   # Header
    values = gsheet.get('values', [])[data_row_start:]  # Data
    if not values:
        print('No data found.')
    else:
        return {"header": header, "values": values}
        