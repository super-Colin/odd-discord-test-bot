
import pandas as pd
import json
import csv
from google.oauth2 import service_account
import pygsheets

# ---
# Use .env file for configuration settings

import os
# Load os module to access other files (.env)
from dotenv import load_dotenv
# Import load_dotenv command from python-dotenv module
# Use the CLI cmd "pip install -U python-dotenv" to make sure you have dotenv installed
load_dotenv()  # Get variables from .env file
SPREADSHEET_ID = os.getenv('GSHEETS_SPREADSHEET_ID')
RANGE_NAME = os.getenv('GSHEETS_RANGE_NAME')
GSHEETS_SPREADSHEET_URL_KEY = os.getenv('GSHEETS_SPREADSHEET_URL_KEY')
# ---


serviceAccountFile = './gCredentials.env.json'
# SCOPES = 

# credentials = service_account.Credentials.from_service_account_file(serviceAccountFile)
# delegatedCredentials = credentials.with_subject('superColin.dev@gmail.com')




# # with open('service_account.json') as source:
# with open('gCredentials.env.json') as source:
#     info = json.load(source)
# credentials = service_account.Credentials.from_service_account_info(info)




# client = pygsheets.authorize(service_account_file='service_account.json')
client = pygsheets.authorize(service_file='gCredentials.env.json')


# sheet_data = client.sheet.get(GSHEETS_SPREADSHEET_URL_KEY)
sheet = client.open_by_key(GSHEETS_SPREADSHEET_URL_KEY)
print(sheet)
wks = sheet.worksheet_by_title('Sheet1')
# print(sheet_data)

print(f"Columns: {wks.cols}")
print(f"Rows: {wks.rows}")


# wks.add_rows(1)
# for row in wks:
#     print(row)


# # If the number of rows within the worksheet is less than the dataframe:
# if wks.rows < df.shape[0]:
#     number_of_rows_to_add = df.shape[0] - wks.rows + 1
#     # Adding the required number of rows
#     wks.add_rows(number_of_rows_to_add)



def delegatedAuth():
  scopes = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
  with open(serviceAccountFile) as source:
    info = json.load(source)
    # credentials = service_account.Credentials.from_service_account_info(info)
    credentials = service_account.Credentials.from_service_account_file(info)
    delegated_credentials = credentials.with_subject('SuperColin.dev@gmail.com', scopes=scopes)
    return delegated_credentials


delegated_credentials = delegatedAuth()

def addRow():
  values = wks.cols * ["Test"]
  # print(f"These are the values which will be appended to the new row: n n {values}")
  wks.add_rows(1)
  # wks.insert_rows( wks.cols, values)

addRow()
# print(client)
