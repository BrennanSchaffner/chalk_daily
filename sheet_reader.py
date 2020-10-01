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
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if os.path.exists('../token.pickle'): ####################################
            switch = True
            with open('../token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    '/home/pi/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            if switch:
                with open('../token.pickle', 'wb') as token: ##############################3
                    pickle.dump(creds, token)
            else:
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)

        # Call the Sheets API
        # try:
        service = build('sheets', 'v4', credentials=creds)
        print(service)
        sheet = service.spreadsheets()
        print(sheet)
        result = sheet.values().get(spreadsheetId=self.spreadsheet_id, range=self.sheet_range).execute()
        print(result)
        values = result.get('values', [])
        print(values)
        # except:
        #     return "failed"

        return values
