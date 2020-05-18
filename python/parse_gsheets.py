""" 
Snippet to read data from google sheets
Set up an API with relevant credentials as mentioned in
https://developers.google.com/sheets/api/quickstart/python?authuser=1
"""

from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import pandas as pd
import numpy as np
import requests
import io

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

creds = None

# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
# If the pickle file is not present the code will attempt to open a new window or tab in your default browser. 
# If you are not already logged into your Google account, you will be prompted to log in. 
# If you are logged into multiple Google accounts, you will be asked to select one account to use for 
# the authorization.
if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Get the id from the url of the sheet (after opening it in the browser)
SAMPLE_SPREADSHEET_ID = '1FA2Ibqk7UjcHXl8wc8vCyH5Ev2GZrGzSyI'
SAMPLE_RANGE_NAME = ['Sheet1!B23:Q35','Sheet1!B58:M72','Sheet2!B147:E176','Sheet1!B179:F195','Sheet3!B201:D215']

# Loop through the ranges and Call the Sheets API
newval = []
for idx in range(len(SAMPLE_RANGE_NAME)):
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME[idx]).execute()
    values = result.get('values', [])
    
    #  Here C1 and C2 are two hierarchical column with C1 as the parent
    c1 = values[0]
    c2temp=values[1:]
    for idx, val in enumerate(c2temp):
        for idx1, val1 in enumerate(val):
            newval.append([c1[idx1],val1])

# Read data from multiple columns into a single column in the dataframe
df = pd.DataFrame(newval, columns=['c1','c2'])
df['c2'].replace('', np.nan, inplace=True)
df = df.dropna()
df.drop_duplicates(inplace=True)