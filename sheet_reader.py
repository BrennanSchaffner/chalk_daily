import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


class SheetReader(object):
    def __init__(self, spreadsheet_id, sheet_range):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_range = sheet_range

    def download_data(self):
        creds = None
        switch = False
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        print('aaaaaaaa')
        if os.path.exists('token.pickle'):
            print('bbbbbbbb')
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if os.path.exists('../token.pickle'): ####################################
            print('cccccccccccc')
            switch = True
            with open('../token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            print('ddddddd')
            if creds and creds.expired and creds.refresh_token:
                print('eeeeeeeee')
                creds.refresh(Request())
            else:
                print('fffffffffff')

                flow = InstalledAppFlow.from_client_secrets_file(
                    '/home/pi/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            if switch:
                print('ggggggggggggg')

                with open('../token.pickle', 'wb') as token: ##############################3
                    pickle.dump(creds, token)
            else:
                print('hhhhhhhhhhhh')
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
        print('iiiiiiii')
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.sheet_range).execute()
        values = result.get('values', [])

        return values
