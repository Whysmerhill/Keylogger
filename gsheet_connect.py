import gspread
from oauth2client.service_account import ServiceAccountCredentials

def gsheetinit(key):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    #sheet = client.open_by_key("Keylogger Demo").sheet1
    sheet = client.open_by_key(key).sheet1

    # Extract and print all of the values
    list_of_hashes = sheet.get_all_records()
    print(list_of_hashes)
    return sheet

#Test

row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
index = 1
sheet = gsheetinit("15okwR0eO_WRlAtIc6HLRgjOQ8rpYerWwMg6-EyCIblI")
sheet.insert_row(row, index)