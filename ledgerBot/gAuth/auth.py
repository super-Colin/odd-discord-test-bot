from __future__ import print_function
from googleapiclient.discovery import build 
from google.oauth2 import service_account
SCOPES = [
'https://www.googleapis.com/auth/spreadsheets',
'https://www.googleapis.com/auth/drive'
]
credentials = service_account.Credentials.from_service_account_file('gCredentials.env.json', scopes=SCOPES)
delegated_credentials = credentials.with_subject('SuperColin.dev@gmail.com', scopes=SCOPES)
spreadsheet_service = build('sheets', 'v4', credentials=credentials)
drive_service = build('drive', 'v3', credentials=credentials)