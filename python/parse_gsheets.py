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
import requests
import io

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Get the id from the url of the sheet (after opening it in the browser)
SAMPLE_SPREADSHEET_ID = '1FA2Ibqk7UjcHXl8wc8vCyH5Ev2GZrGzSyI'
SAMPLE_RANGE_NAME = 'Sheet1!A1:N25'

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

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=SAMPLE_RANGE_NAME).execute()
values = result.get('values', [])

# Read data from multiple columns into a single column in the dataframe
df = pd.DataFrame()
for colList in values:
    df = pd.concat([df, pd.DataFrame([i for i in colList if i])])

df.reset_index(inplace=True, drop=True)