import gspread
from google.oauth2.service_account import Credentials
import tempfile

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

    def add_invoice_row(self, items, total, metadata=None):
        """
        Stores invoice data in a single row:
        - metadata (optional): list with invoice ID, client, date, etc.
        - items: list of tuples/lists (desc, qty, price) or (desc, amount)
        - total: final total value
        """
        row = metadata if metadata else []

        # Flatten item data
        for item in items:
            if isinstance(item, dict):
                desc = item.get("name", "")
                qty = item.get("amount", 1)
                price = item.get("price", 0)
                row.extend([desc, qty, price])
            elif isinstance(item, tuple) or isinstance(item, list):
                row.extend(item)

        row.append(total)

        try:
            self.sheet.append_row(row)
            return True
        except Exception as e:
            print(f"Error adding data to Google Sheets: {e}")
            return False
