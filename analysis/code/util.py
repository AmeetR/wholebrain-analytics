import pandas as pd
import numpy as np
import pickle as pkl 
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


""""
The following three definitions are for the function that reads
the google sheet that has the updated information for all of the 
brains. If we add more columns, change the range name. If the sheet
changes, find the new id and fill in the BRAIN_STATUS as necessary. 
If we want read write access, we should change the SCOPES as required. 
"""
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
BRAIN_STATUS = '1LNAdl2GTLYQfIM9mWFzn4cqAAjIWE5pjiJxkbEyQuQA'
RANGE_NAME = 'Sheet1!A1:K'




def get_brain_status_spreadsheet():
    """
    This is a basic utility function in order to scrape the 
    status brain google sheet so that we don't have to 
    manually fill this in. It will return a pandas dataframe. 
    
    """
    creds = None
    # The file token.pkl stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pkl'):
        with open('token.pkl', 'rb') as token:
            creds = pkl.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pkl', 'wb') as token:
            pkl.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=BRAIN_STATUS,
                                range=RANGE_NAME).execute()
    values = result.get('values', [])
    df = pd.DataFrame(values, index = None)
    return df






