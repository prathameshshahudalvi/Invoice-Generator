import gspread
from google.oauth2.service_account import Credentials
import tempfile
import pandas as pd
import os

class AddInGoogleSheet:
    def __init__(self, credentials_file, spreadsheet_key):
        self.credentials_file = credentials_file
        self.spreadsheet_key = spreadsheet_key
        self.scopes = ["https://www.googleapis.com/auth/spreadsheets"]

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
            tmp.write(self.credentials_file.getvalue())
            tmp_path = tmp.name
        self.creds = Credentials.from_service_account_file(tmp_path, scopes=self.scopes)
        
        self.client = gspread.authorize(self.creds)
        self.sheet = self.client.open_by_key(self.spreadsheet_key).sheet1

    def add_data(self, data):
        try:
            self.sheet.append_row(data)
            return True
        except Exception as e:
            print(f"Error adding data to Google Sheets: {e}")
            return False