# https://pyshark.com/google-sheets-api-using-python/

import gspread
import datetime
from oauth2client.service_account import ServiceAccountCredentials

gc = gspread.service_account(filename="gCredentials.env.json")


# gSheet = gc.open("ledger_test")
gSheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1xTytU9c-UNqh_69wsuMknf7pbFoFFofjtkobxnntEjI/")

mydata = gSheet.sheet1.get_all_records()
print(mydata)



dt_date_format = "%Y-%m-%d"
dt_time_format = "%H:%M:%S"
dt_check_against_day = datetime.datetime.strptime( "2020-01-01", dt_date_format)
dt_check_against_time = datetime.datetime.strptime( "01:01:01", dt_time_format)

def get_dt_date_now():
  return datetime.datetime.today().strftime(dt_date_format)

def get_dt_time_now():
  return datetime.datetime.today().strftime(dt_time_format)

def get_balance(accountName):
  account_balance = -1
  balance_reference_date = dt_check_against_day
  balance_reference_time = dt_check_against_time
  for transaction in mydata:
    transaction_date = datetime.datetime.strptime( transaction["Date"], dt_date_format )
    transaction_time = datetime.datetime.strptime( transaction["Time"], dt_time_format )
    # check if transaction involved the person
    if transaction["To Account"] == accountName:
      print("was to")
      # check if the date was more recent
      if transaction_date > balance_reference_date:
        print("newer then the old to date")
        # check if the time is more recent
        if transaction_time > balance_reference_time:
          balance_reference_time = transaction_time
          account_balance = transaction["To Balance"]
          print("updated balance got newest balance!")
    if transaction["From Account"] == accountName:
      print("was from")
      if transaction_date > balance_reference_date:
        print("newer then the old from date")
        if transaction_time > balance_reference_time:
          balance_reference_time = transaction_time
          account_balance = transaction["From Balance"]
          print("updated balance got newest balance!")
    if account_balance >= 0:
      return account_balance
    if account_balance < 0:
      return "balance not found"


get_balance("Dog") # exZepected output 10


def make_payment(from_account, to_account, amount, description):
  from_balance = get_balance(from_account)
  if from_account < amount:
    return "there are not enough funds in the from_account"
  to_balance = get_balance(to_account)
  if not to_balance > 0:
    to_balance = 0
  new_ledger_entry = {"Date": get_dt_date_now(), "Time": get_dt_time_now(), "To Account": to_account, "From Balance": from_account, "To balance": to_balance, "From Balance": from_balance, "Description":description}
  



# import datetime
# today_now = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")

# d1 = datetime.datetime.strptime("2021-05-22", "%Y-%m-%d")
# d2 = datetime.datetime.strptime("2021-05-21", "%Y-%m-%d")
# print("d1 is greater than d2 : ", d1 > d2)
# print("d1 is less than d2 : ", d1 < d2)
# print("d1 is not equal to d2 : ", d1 != d2)
